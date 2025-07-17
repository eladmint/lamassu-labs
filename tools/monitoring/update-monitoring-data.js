#!/usr/bin/env node

// Example script to update monitoring data in Juno satellite
// This can be run from a backend service or scheduled as a cron job

import { initJuno, setDoc } from '@junobuild/core';

const SATELLITE_ID = 'bvxuo-uaaaa-aaaal-asgua-cai';

async function updateMonitoringData() {
    try {
        // Initialize Juno
        console.log('Initializing Juno connection...');
        const juno = await initJuno({
            satelliteId: SATELLITE_ID
        });

        // Prepare monitoring data
        const timestamp = new Date().toISOString();
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Main monitoring summary
        const monitoringData = {
            timestamp: timestamp,
            network: 'ICP',
            summary: {
                total_contracts: 3,
                healthy_contracts: 2,
                degraded_contracts: 1,
                unhealthy_contracts: 0,
                total_alerts: 2,
                critical_alerts: 0
            }
        };

        // Contract metrics
        const contractMetrics = [
            {
                key: 'hallucination_verifier.aleo',
                data: {
                    program_id: 'hallucination_verifier.aleo',
                    total_transactions: Math.floor(Math.random() * 100) + 200,
                    successful_transactions: Math.floor(Math.random() * 10) + 240,
                    failed_transactions: Math.floor(Math.random() * 5) + 5,
                    average_execution_time: Math.floor(Math.random() * 50) + 120,
                    last_activity: new Date(Date.now() - Math.random() * 3600 * 1000).toISOString(),
                    current_stake: 500000,
                    active_agents: Math.floor(Math.random() * 10) + 45,
                    gas_used_24h: Math.floor(Math.random() * 5000000) + 20000000,
                    health_status: 'healthy'
                }
            },
            {
                key: 'agent_registry_v2.aleo',
                data: {
                    program_id: 'agent_registry_v2.aleo',
                    total_transactions: Math.floor(Math.random() * 100) + 400,
                    successful_transactions: Math.floor(Math.random() * 20) + 400,
                    failed_transactions: Math.floor(Math.random() * 3) + 2,
                    average_execution_time: Math.floor(Math.random() * 30) + 80,
                    last_activity: new Date(Date.now() - Math.random() * 1800 * 1000).toISOString(),
                    current_stake: 750000,
                    active_agents: Math.floor(Math.random() * 10) + 60,
                    gas_used_24h: Math.floor(Math.random() * 8000000) + 40000000,
                    health_status: 'healthy'
                }
            },
            {
                key: 'trust_verifier_v2.aleo',
                data: {
                    program_id: 'trust_verifier_v2.aleo',
                    total_transactions: Math.floor(Math.random() * 50) + 150,
                    successful_transactions: Math.floor(Math.random() * 10) + 170,
                    failed_transactions: Math.floor(Math.random() * 5) + 5,
                    average_execution_time: Math.floor(Math.random() * 50) + 200,
                    last_activity: new Date(Date.now() - 8 * 3600 * 1000).toISOString(),
                    current_stake: 200000,
                    active_agents: Math.floor(Math.random() * 5) + 35,
                    gas_used_24h: Math.floor(Math.random() * 3000000) + 15000000,
                    health_status: 'degraded'
                }
            }
        ];

        // Active alerts
        const alerts = [];
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Check for degraded contracts and create alerts
        contractMetrics.forEach(contract => {
            if (contract.data.health_status === 'degraded') {
                const lastActivity = new Date(contract.data.last_activity);
                const hoursAgo = (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60);
<<<<<<< HEAD

=======
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                if (hoursAgo > 6) {
                    alerts.push({
                        key: `alert_${contract.key}_inactivity`,
                        data: {
                            severity: 'warning',
                            contract: contract.key,
                            message: `No activity for ${hoursAgo.toFixed(1)} hours`,
                            timestamp: timestamp
                        }
                    });
                }
<<<<<<< HEAD

=======
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                if (contract.data.average_execution_time > 200) {
                    alerts.push({
                        key: `alert_${contract.key}_performance`,
                        data: {
                            severity: 'warning',
                            contract: contract.key,
                            message: 'Average execution time above threshold',
                            timestamp: timestamp
                        }
                    });
                }
            }
        });

        // Update monitoring summary
        console.log('Updating monitoring summary...');
        await setDoc({
            collection: 'monitoring_data',
            doc: {
                key: 'current',
                data: monitoringData
            }
        });

        // Update contract metrics
        console.log('Updating contract metrics...');
        for (const metric of contractMetrics) {
            await setDoc({
                collection: 'contract_metrics',
                doc: {
                    key: metric.key,
                    data: metric.data
                }
            });
        }

        // Update alerts
        if (alerts.length > 0) {
            console.log(`Updating ${alerts.length} alerts...`);
            for (const alert of alerts) {
                await setDoc({
                    collection: 'alerts',
                    doc: {
                        key: alert.key,
                        data: alert.data
                    }
                });
            }
        }

        console.log('✅ Monitoring data updated successfully!');
        console.log(`   - Contracts: ${contractMetrics.length}`);
        console.log(`   - Alerts: ${alerts.length}`);
        console.log(`   - Timestamp: ${timestamp}`);

    } catch (error) {
        console.error('❌ Failed to update monitoring data:', error);
        process.exit(1);
    }
}

// Run the update
updateMonitoringData();

// Example: Schedule updates every 5 minutes
<<<<<<< HEAD
// setInterval(updateMonitoringData, 5 * 60 * 1000);
=======
// setInterval(updateMonitoringData, 5 * 60 * 1000);
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
