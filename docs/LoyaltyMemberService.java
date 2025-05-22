package com.optum.loyalty.member.service;

import com.optum.loyalty.member.dto.MemberDTO;
import com.optum.loyalty.member.dto.FamilyMemberDTO;
import com.optum.loyalty.member.entity.LoyaltyMember;
import com.optum.loyalty.member.entity.FamilyMember;
import com.optum.loyalty.member.repository.LoyaltyMemberRepository;
import com.optum.loyalty.member.repository.FamilyMemberRepository;
import com.optum.loyalty.member.kafka.MemberEventProducer;
import com.optum.loyalty.member.exception.MemberNotFoundException;
import com.optum.loyalty.member.exception.DualEligibilityException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Service class for managing loyalty member operations
 * Handles member enrollment, family relationships, and eligibility processing
 * 
 * @author Taj Mahal Team
 * @version 1.2.0
 */
@Service
@Transactional
public class LoyaltyMemberService {
    
    private static final Logger logger = LoggerFactory.getLogger(LoyaltyMemberService.class);
    
    @Autowired
    private LoyaltyMemberRepository memberRepository;
    
    @Autowired
    private FamilyMemberRepository familyMemberRepository;
    
    @Autowired
    private MemberEventProducer memberEventProducer;
    
    /**
     * Retrieves member by UHC member ID
     * @param uhcMemberId UnitedHealthcare member identifier
     * @return MemberDTO containing member details
     * @throws MemberNotFoundException if member not found
     */
    public MemberDTO getMemberByUhcId(String uhcMemberId) {
        logger.info("Retrieving member with UHC ID: {}", uhcMemberId);
        
        Optional<LoyaltyMember> member = memberRepository.findByUhcMemberId(uhcMemberId);
        if (member.isEmpty()) {
            logger.warn("Member not found for UHC ID: {}", uhcMemberId);
            throw new MemberNotFoundException("Member not found with UHC ID: " + uhcMemberId);
        }
        
        return convertToDTO(member.get());
    }
    
    /**
     * Enrolls a new member in the loyalty platform
     * Handles partner/client affiliation and family assignment
     * @param memberDTO Member enrollment details
     * @return Created member DTO
     */
    public MemberDTO enrollMember(MemberDTO memberDTO) {
        logger.info("Enrolling new member: UHC ID {}, Partner: {}, Client: {}", 
                   memberDTO.getUhcMemberId(), memberDTO.getPartner(), memberDTO.getClient());
        
        // Check for existing member
        if (memberRepository.existsByUhcMemberId(memberDTO.getUhcMemberId())) {
            logger.error("Member already exists with UHC ID: {}", memberDTO.getUhcMemberId());
            throw new IllegalArgumentException("Member already enrolled with UHC ID: " + memberDTO.getUhcMemberId());
        }
        
        // Create new member entity
        LoyaltyMember member = new LoyaltyMember();
        member.setMemberId(UUID.randomUUID().toString());
        member.setUhcMemberId(memberDTO.getUhcMemberId());
        member.setPartner(memberDTO.getPartner());
        member.setClient(memberDTO.getClient());
        member.setAffiliation(determineAffiliation(memberDTO));
        member.setEnrollmentDate(LocalDate.now());
        member.setStatus("ACTIVE");
        member.setSpouseAssignmentStatus("PENDING");
        member.setCreatedDate(LocalDateTime.now());
        
        // Handle family assignment
        if (memberDTO.getFamilyId() != null && !memberDTO.getFamilyId().isEmpty()) {
            member.setFamilyId(memberDTO.getFamilyId());
        } else {
            member.setFamilyId(UUID.randomUUID().toString());
        }
        
        // Save member
        LoyaltyMember savedMember = memberRepository.save(member);
        logger.info("Successfully enrolled member: {}", savedMember.getMemberId());
        
        // Publish enrollment event to Kafka
        memberEventProducer.publishMemberEnrollmentEvent(savedMember);
        
        // Process spouse assignment if applicable
        if (memberDTO.getSpouseUhcId() != null) {
            processSpouseAssignment(savedMember, memberDTO.getSpouseUhcId());
        }
        
        return convertToDTO(savedMember);
    }
    
    /**
     * Processes spouse assignment for family enrollment
     * @param primaryMember Primary member in family
     * @param spouseUhcId Spouse's UHC member ID
     */
    private void processSpouseAssignment(LoyaltyMember primaryMember, String spouseUhcId) {
        logger.info("Processing spouse assignment for primary member: {}, spouse UHC ID: {}", 
                   primaryMember.getMemberId(), spouseUhcId);
        
        try {
            // Find spouse by UHC ID
            Optional<LoyaltyMember> spouse = memberRepository.findByUhcMemberId(spouseUhcId);
            
            if (spouse.isPresent()) {
                LoyaltyMember spouseMember = spouse.get();
                
                // Update spouse's family ID
                spouseMember.setFamilyId(primaryMember.getFamilyId());
                spouseMember.setSpouseAssignmentStatus("COMPLETED");
                spouseMember.setSpouseAssignmentDate(LocalDateTime.now());
                memberRepository.save(spouseMember);
                
                // Create family member relationships
                createFamilyMemberRelationship(primaryMember.getFamilyId(), 
                                             primaryMember.getMemberId(), "PRIMARY", true);
                createFamilyMemberRelationship(primaryMember.getFamilyId(), 
                                             spouseMember.getMemberId(), "SPOUSE", false);
                
                // Update primary member status
                primaryMember.setSpouseAssignmentStatus("COMPLETED");
                primaryMember.setSpouseAssignmentDate(LocalDateTime.now());
                memberRepository.save(primaryMember);
                
                // Publish family event
                memberEventProducer.publishFamilyAssignmentEvent(primaryMember.getFamilyId(), 
                                                               primaryMember.getMemberId(), 
                                                               spouseMember.getMemberId());
                
                logger.info("Successfully completed spouse assignment for family: {}", 
                           primaryMember.getFamilyId());
            } else {
                // Spouse not found - mark for retry
                primaryMember.setSpouseAssignmentStatus("SPOUSE_NOT_FOUND");
                memberRepository.save(primaryMember);
                
                logger.warn("Spouse not found for UHC ID: {}, will retry later", spouseUhcId);
            }
            
        } catch (Exception e) {
            // Handle spouse assignment failure
            primaryMember.setSpouseAssignmentStatus("FAILED");
            memberRepository.save(primaryMember);
            
            logger.error("Spouse assignment failed for member: {}, error: {}", 
                        primaryMember.getMemberId(), e.getMessage(), e);
        }
    }
    
    /**
     * Creates family member relationship record
     */
    private void createFamilyMemberRelationship(String familyId, String memberId, 
                                              String relationshipType, boolean isPrimary) {
        FamilyMember familyMember = new FamilyMember();
        familyMember.setFamilyMemberId(UUID.randomUUID().toString());
        familyMember.setFamilyId(familyId);
        familyMember.setMemberId(memberId);
        familyMember.setRelationshipType(relationshipType);
        familyMember.setPrimaryMember(isPrimary);
        familyMember.setCreatedDate(LocalDateTime.now());
        
        familyMemberRepository.save(familyMember);
    }
    
    /**
     * Determines member affiliation based on partner and client
     */
    private String determineAffiliation(MemberDTO memberDTO) {
        String partner = memberDTO.getPartner();
        String client = memberDTO.getClient();
        
        if ("UnitedHealthcare".equals(partner)) {
            if ("INDIVIDUAL".equals(client)) {
                return "UHC_INDIVIDUAL";
            } else if ("FAMILY".equals(client)) {
                return "UHC_FAMILY_PRIMARY";
            }
        } else if ("Optum".equals(partner)) {
            if ("EMPLOYEE".equals(client)) {
                return "OPTUM_EMPLOYEE";
            } else if ("CONTRACTOR".equals(client)) {
                return "OPTUM_CONTRACTOR";
            }
        }
        
        return "UNKNOWN_AFFILIATION";
    }
    
    /**
     * Converts entity to DTO
     */
    private MemberDTO convertToDTO(LoyaltyMember member) {
        MemberDTO dto = new MemberDTO();
        dto.setMemberId(member.getMemberId());
        dto.setUhcMemberId(member.getUhcMemberId());
        dto.setPartner(member.getPartner());
        dto.setClient(member.getClient());
        dto.setAffiliation(member.getAffiliation());
        dto.setEnrollmentDate(member.getEnrollmentDate());
        dto.setStatus(member.getStatus());
        dto.setFamilyId(member.getFamilyId());
        dto.setSpouseAssignmentStatus(member.getSpouseAssignmentStatus());
        return dto;
    }
}