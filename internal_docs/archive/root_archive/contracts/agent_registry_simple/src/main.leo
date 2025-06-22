// Simplified Agent Registry for Aleo
program agent_registry_simple.aleo {
    
    // Agent metrics mapping
    mapping agent_scores: field => u32;
    
    // Agent stakes mapping  
    mapping agent_stakes: field => u64;
    
    // Agent owners mapping
    mapping agent_owners: field => address;
    
    // Verification result (not a record, just a struct)
    struct VerificationResult {
        agent_id: field,
        score: u32,
        verified: bool,
        timestamp: u32,
    }
    
    // Register agent and return verification
    transition register_agent(
        public agent_id: field,
        public stake_amount: u64,
        private accuracy: u32,
        private tasks_completed: u32,
        public current_height: u32
    ) -> VerificationResult {
        
        // Calculate simple score
        let base_score: u32 = accuracy;
        let bonus: u32 = tasks_completed > 100u32 ? 1000u32 : 0u32;
        let total_score: u32 = base_score + bonus;
        
        // Create result
        let result: VerificationResult = VerificationResult {
            agent_id: agent_id,
            score: total_score,
            verified: total_score > 7000u32,
            timestamp: current_height,
        };
        
        return result;
    }
    
    // Verify agent performance
    transition verify_agent(
        public agent_id: field,
        private new_accuracy: u32,
        public current_height: u32
    ) -> VerificationResult {
        
        let result: VerificationResult = VerificationResult {
            agent_id: agent_id,
            score: new_accuracy,
            verified: new_accuracy > 7000u32,
            timestamp: current_height,
        };
        
        return result;
    }
}