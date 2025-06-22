// The MIT License (MIT)
// Copyright (c) 2025 Lamassu Labs
// Version 2.0 - Security Enhanced

program agent_registry_v2.aleo {
    // Constants for safe math
    const MAX_U32: u32 = 4294967295u32;
    const BASIS_POINTS: u32 = 10000u32;
    
    // Agent performance metrics (private)
    struct AgentMetrics {
        accuracy: u32,          // 0-10000 basis points (100.00%)
        latency: u32,           // milliseconds
        tasks_completed: u32,   // total tasks
        success_rate: u32,      // 0-10000 basis points
    }
    
    // Public agent profile
    struct AgentProfile {
        agent_id: field,
        owner: address,
        stake_amount: u64,
        verified: bool,
        performance_hash: field,
        created_at: u32,        // block height
        updated_at: u32,        // block height
    }
    
    // Verification proof
    struct VerificationProof {
        agent_id: field,
        timestamp: u32,
        performance_score: u32,   // 0-10000 basis points
        meets_threshold: bool,
        verifier: address,
    }
    
    // Staking record
    record StakeRecord {
        owner: address,
        gates: u64,
        agent_id: field,
        staked_at: u32,
        locked_until: u32,      // Minimum lock period
    }
    
    // Withdrawal record
    record WithdrawalRecord {
        owner: address,
        gates: u64,
        agent_id: field,
        withdrawn_at: u32,
    }
    
    // Mapping of agent profiles
    mapping agents: field => AgentProfile;
    
    // Mapping of stakes
    mapping stakes: field => u64;
    
    // Mapping to check if agent exists
    mapping agent_exists: field => bool;
    
    // Mapping of agent owners
    mapping agent_owners: field => address;
    
    // Register a new agent with hidden metrics
    transition register_agent(
        public agent_id: field,
        private metrics: AgentMetrics,
        public stake_amount: u64,
        public current_height: u32
    ) -> (VerificationProof, StakeRecord) {
        // Validate metrics ranges
        assert(metrics.accuracy <= BASIS_POINTS);
        assert(metrics.success_rate <= BASIS_POINTS);
        assert(metrics.latency > 0u32);
        
        // Calculate performance score privately with safe math
        let performance_score: u32 = calculate_performance_score_safe(metrics);
        
        // Create verification proof
        let proof: VerificationProof = VerificationProof {
            agent_id: agent_id,
            timestamp: current_height,
            performance_score: performance_score,
            meets_threshold: performance_score >= 7000u32, // 70%
            verifier: self.caller,
        };
        
        // Create stake record with lock period
        let lock_period: u32 = 100u32; // 100 blocks minimum
        let stake: StakeRecord = StakeRecord {
            owner: self.caller,
            gates: stake_amount,
            agent_id: agent_id,
            staked_at: current_height,
            locked_until: current_height + lock_period,
        };
        
        return (proof, stake);
    }
    
    // Update existing agent (only owner can update)
    transition update_agent(
        public agent_id: field,
        private metrics: AgentMetrics,
        public current_height: u32
    ) -> VerificationProof {
        // In finalize, will check that caller is owner
        let performance_score: u32 = calculate_performance_score_safe(metrics);
        
        return VerificationProof {
            agent_id: agent_id,
            timestamp: current_height,
            performance_score: performance_score,
            meets_threshold: performance_score >= 7000u32,
            verifier: self.caller,
        };
    }
    
    // Verify agent performance without revealing metrics
    transition verify_performance(
        public agent_id: field,
        private metrics: AgentMetrics,
        public threshold: u32,
        public current_height: u32
    ) -> VerificationProof {
        assert(threshold <= BASIS_POINTS);
        
        let performance_score: u32 = calculate_performance_score_safe(metrics);
        
        return VerificationProof {
            agent_id: agent_id,
            timestamp: current_height,
            performance_score: performance_score,
            meets_threshold: performance_score >= threshold,
            verifier: self.caller,
        };
    }
    
    // Add stake to existing agent
    transition add_stake(
        public agent_id: field,
        public additional_stake: u64,
        public current_height: u32
    ) -> StakeRecord {
        let lock_period: u32 = 100u32;
        
        return StakeRecord {
            owner: self.caller,
            gates: additional_stake,
            agent_id: agent_id,
            staked_at: current_height,
            locked_until: current_height + lock_period,
        };
    }
    
    // Withdraw stake (only after lock period)
    transition withdraw_stake(
        public agent_id: field,
        public amount: u64,
        public current_height: u32,
        private stake_record: StakeRecord
    ) -> WithdrawalRecord {
        // Verify ownership
        assert_eq(stake_record.owner, self.caller);
        assert_eq(stake_record.agent_id, agent_id);
        
        // Check lock period
        assert(current_height >= stake_record.locked_until);
        
        // Verify amount
        assert(amount <= stake_record.gates);
        
        return WithdrawalRecord {
            owner: self.caller,
            gates: amount,
            agent_id: agent_id,
            withdrawn_at: current_height,
        };
    }
    
    // Private helper function with safe math
    function calculate_performance_score_safe(metrics: AgentMetrics) -> u32 {
        // Weighted scoring with basis points: 
        // 40% accuracy, 20% success rate, 20% latency, 20% experience
        
        // Safe multiplication with overflow checks
        let accuracy_score: u32 = safe_multiply(metrics.accuracy, 4000u32) / BASIS_POINTS;
        let success_score: u32 = safe_multiply(metrics.success_rate, 2000u32) / BASIS_POINTS;
        
        // Latency scoring (lower is better, max 1000ms)
        let latency_score: u32 = 0u32;
        if metrics.latency < 100u32 {
            latency_score = BASIS_POINTS;
        } else if metrics.latency < 500u32 {
            latency_score = 8000u32;
        } else if metrics.latency < 1000u32 {
            latency_score = 6000u32;
        } else {
            latency_score = 4000u32;
        }
        let latency_weight: u32 = safe_multiply(latency_score, 2000u32) / BASIS_POINTS;
        
        // Experience scoring (more tasks = better)
        let experience_score: u32 = 0u32;
        if metrics.tasks_completed > 1000u32 {
            experience_score = BASIS_POINTS;
        } else if metrics.tasks_completed > 500u32 {
            experience_score = 8000u32;
        } else if metrics.tasks_completed > 100u32 {
            experience_score = 6000u32;
        } else {
            experience_score = 4000u32;
        }
        let experience_weight: u32 = safe_multiply(experience_score, 2000u32) / BASIS_POINTS;
        
        // Safe addition
        let total: u32 = safe_add(safe_add(accuracy_score, success_score), 
                                  safe_add(latency_weight, experience_weight));
        
        return total;
    }
    
    // Safe multiplication with overflow check
    function safe_multiply(a: u32, b: u32) -> u32 {
        // Simple overflow check - in production use more sophisticated method
        assert(b == 0u32 || a <= MAX_U32 / b);
        return a * b;
    }
    
    // Safe addition with overflow check
    function safe_add(a: u32, b: u32) -> u32 {
        assert(a <= MAX_U32 - b);
        return a + b;
    }
    
    // Finalize functions for state updates
    finalize register_agent(agent_id: field, owner: address, stake: u64, height: u32) {
        // Check if agent already exists
        let exists: bool = Mapping::get_or_use(agent_exists, agent_id, false);
        assert(!exists);
        
        // Create profile
        let profile: AgentProfile = AgentProfile {
            agent_id: agent_id,
            owner: owner,
            stake_amount: stake,
            verified: true,
            performance_hash: BHP256::hash(agent_id),
            created_at: height,
            updated_at: height,
        };
        
        // Update mappings
        Mapping::set(agents, agent_id, profile);
        Mapping::set(agent_exists, agent_id, true);
        Mapping::set(agent_owners, agent_id, owner);
        Mapping::set(stakes, agent_id, stake);
    }
    
    finalize update_agent(agent_id: field, caller: address, height: u32) {
        // Verify ownership
        let owner: address = Mapping::get(agent_owners, agent_id);
        assert_eq(owner, caller);
        
        // Update timestamp
        let mut profile: AgentProfile = Mapping::get(agents, agent_id);
        profile.updated_at = height;
        Mapping::set(agents, agent_id, profile);
    }
    
    finalize add_stake(agent_id: field, amount: u64) {
        let current_stake: u64 = Mapping::get_or_use(stakes, agent_id, 0u64);
        let new_stake: u64 = current_stake + amount;
        Mapping::set(stakes, agent_id, new_stake);
    }
    
    finalize withdraw_stake(agent_id: field, amount: u64) {
        let current_stake: u64 = Mapping::get(stakes, agent_id);
        assert(current_stake >= amount);
        let new_stake: u64 = current_stake - amount;
        Mapping::set(stakes, agent_id, new_stake);
    }
}