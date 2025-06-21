// The MIT License (MIT)
// Copyright (c) 2025 Lamassu Labs

program agent_registry.aleo {
    // Agent performance metrics (private)
    struct AgentMetrics {
        accuracy: u32,          // 0-100 percentage
        latency: u32,           // milliseconds
        tasks_completed: u32,   // total tasks
        success_rate: u32,      // 0-100 percentage
    }
    
    // Public agent profile
    struct AgentProfile {
        agent_id: field,
        owner: address,
        stake_amount: u64,
        verified: bool,
        performance_hash: field,  // Hash of private metrics
    }
    
    // Verification proof
    struct VerificationProof {
        agent_id: field,
        timestamp: u32,
        performance_score: u32,   // 0-100 composite score
        meets_threshold: bool,
    }
    
    // Staking record
    record StakeRecord {
        owner: address,
        gates: u64,
        agent_id: field,
        staked_at: u32,
    }
    
    // Mapping of agent profiles
    mapping agents: field => AgentProfile;
    
    // Mapping of stakes
    mapping stakes: field => u64;
    
    // Register a new agent with hidden metrics
    transition register_agent(
        public agent_id: field,
        private metrics: AgentMetrics,
        public stake_amount: u64
    ) -> (VerificationProof, StakeRecord) {
        // Calculate performance score privately
        let performance_score: u32 = calculate_performance_score(metrics);
        
        // Create verification proof
        let proof: VerificationProof = VerificationProof {
            agent_id: agent_id,
            timestamp: 0u32, // Would use block timestamp in production
            performance_score: performance_score,
            meets_threshold: performance_score >= 70u32,
        };
        
        // Create stake record
        let stake: StakeRecord = StakeRecord {
            owner: self.caller,
            gates: stake_amount,
            agent_id: agent_id,
            staked_at: 0u32, // Would use block timestamp
        };
        
        return (proof, stake);
    }
    
    // Verify agent performance without revealing metrics
    transition verify_performance(
        public agent_id: field,
        private metrics: AgentMetrics,
        public threshold: u32
    ) -> VerificationProof {
        let performance_score: u32 = calculate_performance_score(metrics);
        
        return VerificationProof {
            agent_id: agent_id,
            timestamp: 0u32,
            performance_score: performance_score,
            meets_threshold: performance_score >= threshold,
        };
    }
    
    // Update agent stake
    transition update_stake(
        public agent_id: field,
        public additional_stake: u64
    ) -> StakeRecord {
        return StakeRecord {
            owner: self.caller,
            gates: additional_stake,
            agent_id: agent_id,
            staked_at: 0u32,
        };
    }
    
    // Private helper function to calculate composite score
    function calculate_performance_score(metrics: AgentMetrics) -> u32 {
        // Weighted scoring: 
        // 40% accuracy, 20% success rate, 20% latency, 20% experience
        let accuracy_weight: u32 = metrics.accuracy * 40u32 / 100u32;
        let success_weight: u32 = metrics.success_rate * 20u32 / 100u32;
        
        // Latency scoring (lower is better, max 1000ms)
        let latency_score: u32 = 0u32;
        if metrics.latency < 100u32 {
            latency_score = 100u32;
        } else if metrics.latency < 500u32 {
            latency_score = 80u32;
        } else if metrics.latency < 1000u32 {
            latency_score = 60u32;
        } else {
            latency_score = 40u32;
        }
        let latency_weight: u32 = latency_score * 20u32 / 100u32;
        
        // Experience scoring (more tasks = better)
        let experience_score: u32 = 0u32;
        if metrics.tasks_completed > 1000u32 {
            experience_score = 100u32;
        } else if metrics.tasks_completed > 500u32 {
            experience_score = 80u32;
        } else if metrics.tasks_completed > 100u32 {
            experience_score = 60u32;
        } else {
            experience_score = 40u32;
        }
        let experience_weight: u32 = experience_score * 20u32 / 100u32;
        
        return accuracy_weight + success_weight + latency_weight + experience_weight;
    }
}