// The 'agent_registry' program for managing AI agent registration and performance tracking
program agent_registry_v2.aleo {
    
    // Agent registration record - stores agent details privately
    record AgentRecord {
        owner: address,
        agent_id: field,
        stake_amount: u64,
        performance_score: u32,
        registration_height: u32,
    }
    
    // Agent performance metrics
    struct AgentMetrics {
        accuracy_rate: u32,      // Basis points (0-10000)
        success_rate: u32,       // Basis points (0-10000)  
        avg_latency_ms: u32,     // Milliseconds
        total_executions: u32,   // Total number of executions
    }
    
    // Performance verification result
    struct PerformanceResult {
        agent_id: field,
        score: u32,              // 0-10000 basis points
        verified: bool,
        timestamp: u32,
    }
    
    // Constants for validation
    const MIN_STAKE: u64 = 1000u64;           // Minimum stake amount
    const MAX_STAKE: u64 = 1000000000u64;     // Maximum stake amount (1B)
    const BASIS_POINTS: u32 = 10000u32;       // 100% in basis points
    const MAX_LATENCY: u32 = 10000u32;        // 10 seconds max latency
    
    // Register a new AI agent with stake
    transition register_agent(
        agent_id: field,
        stake_amount: u64,
        initial_metrics: AgentMetrics,
        registration_height: u32,
    ) -> AgentRecord {
        // Validate stake amount
        assert(stake_amount >= MIN_STAKE);
        assert(stake_amount <= MAX_STAKE);
        
        // Validate metrics
        assert(initial_metrics.accuracy_rate <= BASIS_POINTS);
        assert(initial_metrics.success_rate <= BASIS_POINTS);
        assert(initial_metrics.avg_latency_ms <= MAX_LATENCY);
        
        // Calculate initial performance score
        let score: u32 = calc_performance_score(initial_metrics);
        
        // Create and return agent record
        return AgentRecord {
            owner: self.caller,
            agent_id: agent_id,
            stake_amount: stake_amount,
            performance_score: score,
            registration_height: registration_height,
        };
    }
    
    // Verify agent performance and update score
    transition verify_agent(
        agent: AgentRecord,
        new_metrics: AgentMetrics,
        current_height: u32,
    ) -> (AgentRecord, PerformanceResult) {
        // Ensure caller owns the agent
        assert_eq(agent.owner, self.caller);
        
        // Validate new metrics
        assert(new_metrics.accuracy_rate <= BASIS_POINTS);
        assert(new_metrics.success_rate <= BASIS_POINTS);
        assert(new_metrics.avg_latency_ms <= MAX_LATENCY);
        assert(new_metrics.total_executions > 0u32);
        
        // Calculate new performance score
        let new_score: u32 = calc_performance_score(new_metrics);
        
        // Create updated agent record
        let updated_agent: AgentRecord = AgentRecord {
            owner: agent.owner,
            agent_id: agent.agent_id,
            stake_amount: agent.stake_amount,
            performance_score: new_score,
            registration_height: agent.registration_height,
        };
        
        // Create performance result
        let result: PerformanceResult = PerformanceResult {
            agent_id: agent.agent_id,
            score: new_score,
            verified: true,
            timestamp: current_height,
        };
        
        return (updated_agent, result);
    }
    
    // Update agent stake
    transition update_stake(
        agent: AgentRecord,
        new_stake_amount: u64,
    ) -> AgentRecord {
        // Ensure caller owns the agent
        assert_eq(agent.owner, self.caller);
        
        // Validate new stake amount
        assert(new_stake_amount >= MIN_STAKE);
        assert(new_stake_amount <= MAX_STAKE);
        
        // Return updated agent record
        return AgentRecord {
            owner: agent.owner,
            agent_id: agent.agent_id,
            stake_amount: new_stake_amount,
            performance_score: agent.performance_score,
            registration_height: agent.registration_height,
        };
    }
    
    // Transfer agent ownership
    transition transfer_agent(
        agent: AgentRecord,
        new_owner: address,
    ) -> AgentRecord {
        // Ensure caller owns the agent
        assert_eq(agent.owner, self.caller);
        
        // Return agent with new owner
        return AgentRecord {
            owner: new_owner,
            agent_id: agent.agent_id,
            stake_amount: agent.stake_amount,
            performance_score: agent.performance_score,
            registration_height: agent.registration_height,
        };
    }
    
    // Private helper function to calculate performance score
    function calc_performance_score(metrics: AgentMetrics) -> u32 {
        // Weighted scoring with basis points: 
        // 40% accuracy, 20% success rate, 20% latency, 20% experience
        
        // Accuracy component (40% weight)
        let accuracy_component: u32 = (metrics.accuracy_rate * 4u32) / 10u32;
        
        // Success rate component (20% weight)
        let success_component: u32 = (metrics.success_rate * 2u32) / 10u32;
        
        // Latency component (20% weight) - inverse scoring
        let latency_score: u32 = 0u32;
        if (metrics.avg_latency_ms < 100u32) {
            latency_score = BASIS_POINTS;
        } else if (metrics.avg_latency_ms < 500u32) {
            latency_score = 8000u32;
        } else if (metrics.avg_latency_ms < 1000u32) {
            latency_score = 6000u32;
        } else if (metrics.avg_latency_ms < 5000u32) {
            latency_score = 4000u32;
        } else {
            latency_score = 2000u32;
        }
        let latency_component: u32 = (latency_score * 2u32) / 10u32;
        
        // Experience component (20% weight) - based on execution count
        let exp_score: u32 = 0u32;
        if (metrics.total_executions >= 10000u32) {
            exp_score = BASIS_POINTS;
        } else if (metrics.total_executions >= 1000u32) {
            exp_score = 8000u32;
        } else if (metrics.total_executions >= 100u32) {
            exp_score = 6000u32;
        } else if (metrics.total_executions >= 10u32) {
            exp_score = 4000u32;
        } else {
            exp_score = 2000u32;
        }
        let exp_component: u32 = (exp_score * 2u32) / 10u32;
        
        // Calculate total score
        let total_score: u32 = accuracy_component + success_component + latency_component + exp_component;
        
        // Ensure score doesn't exceed maximum
        if (total_score > BASIS_POINTS) {
            return BASIS_POINTS;
        }
        
        return total_score;
    }
}