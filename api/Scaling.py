import kubernetes
from kubernetes import client, config
from typing import Dict, Any, List
import asyncio
import aiohttp
import json
import time
import os

class QuantumScaler:
    def __init__(self, config: Dict[str, Any], test_mode: bool = True):
        self.config = config
        self.test_mode = test_mode
        self.min_replicas = config.get('MIN_REPLICAS', 2)
        self.max_replicas = config.get('MAX_REPLICAS', 10)
        self.target_cpu_utilization = config.get('TARGET_CPU_UTILIZATION', 70)
        self.scaling_cooldown = config.get('SCALING_COOLDOWN', 300)
        self.k8s_core_v1 = None
        self.k8s_apps_v1 = None
        
        if not self.test_mode:
            self._initialize_kubernetes()

    def _initialize_kubernetes(self):
        """Initialize Kubernetes client"""
        try:
            config.load_incluster_config()
        except kubernetes.config.ConfigException:
            try:
                config.load_kube_config()
            except Exception as e:
                print(f"Warning: Kubernetes config not found. Running in limited mode: {str(e)}")
                self.test_mode = True
                return
        
        self.k8s_core_v1 = client.CoreV1Api()
        self.k8s_apps_v1 = client.AppsV1Api()

    async def monitor_and_scale(self):
        """Monitor system metrics and scale accordingly"""
        if self.test_mode:
            return {
                'status': 'test_mode',
                'replicas': self.min_replicas,
                'cpu_utilization': 50,
                'memory_utilization': 40
            }

        while True:
            try:
                metrics = await self._collect_metrics()
                if self._should_scale(metrics):
                    await self._scale_deployment(metrics)
                
                await self._update_status(metrics)
                
            except Exception as e:
                print(f"Scaling error: {str(e)}")
            
            await asyncio.sleep(60)

    async def _collect_metrics(self) -> Dict[str, Any]:
        """Collect system metrics"""
        if self.test_mode:
            return {
                'cpu_utilization': 50,
                'memory_utilization': 40,
                'active_pods': self.min_replicas,
                'pending_requests': 0,
                'latency': 20
            }

        pods = self.k8s_core_v1.list_namespaced_pod(
            namespace="default",
            label_selector="app=quantum-api"
        )
        
        metrics = {
            'cpu_utilization': await self._get_cpu_utilization(),
            'memory_utilization': await self._get_memory_utilization(),
            'active_pods': len(pods.items),
            'pending_requests': await self._get_pending_requests(),
            'latency': await self._get_average_latency()
        }
        
        return metrics

    def _should_scale(self, metrics: Dict[str, Any]) -> bool:
        """Determine if scaling is needed"""
        return (
            metrics['cpu_utilization'] > self.target_cpu_utilization or
            metrics['latency'] > self.config.get('LATENCY_THRESHOLD', 50) or
            metrics['pending_requests'] > self.config.get('MAX_PENDING_REQUESTS', 100)
        )

    async def _scale_deployment(self, metrics: Dict[str, Any]):
        """Scale the deployment based on metrics"""
        current_replicas = metrics['active_pods']
        
        if metrics['cpu_utilization'] > self.target_cpu_utilization:
            new_replicas = min(
                current_replicas + 1,
                self.max_replicas
            )
        else:
            new_replicas = max(
                current_replicas - 1,
                self.min_replicas
            )
        
        if new_replicas != current_replicas:
            deployment = self.k8s_apps_v1.read_namespaced_deployment(
                name="quantum-api",
                namespace="default"
            )
            deployment.spec.replicas = new_replicas
            
            self.k8s_apps_v1.patch_namespaced_deployment(
                name="quantum-api",
                namespace="default",
                body=deployment
            )
            
            print(f"Scaled deployment to {new_replicas} replicas")

    async def _get_cpu_utilization(self) -> float:
        """Get average CPU utilization"""
        return 50.0

    async def _get_memory_utilization(self) -> float:
        """Get average memory utilization"""
        return 40.0

    async def _get_pending_requests(self) -> int:
        """Get number of pending requests"""
        return 0

    async def _get_average_latency(self) -> float:
        """Get average request latency"""
        return 20.0

    async def _update_status(self, metrics: Dict[str, Any]):
        """Update deployment status"""
        status = {
            'timestamp': time.time(),
            'metrics': metrics,
            'scaling_status': {
                'current_replicas': metrics['active_pods'],
                'min_replicas': self.min_replicas,
                'max_replicas': self.max_replicas,
                'target_cpu_utilization': self.target_cpu_utilization
            }
        }
        
        configmap = client.V1ConfigMap(
            metadata=client.V1ObjectMeta(name="quantum-api-status"),
            data={'status': json.dumps(status)}
        )
        
        try:
            self.k8s_core_v1.replace_namespaced_config_map(
                name="quantum-api-status",
                namespace="default",
                body=configmap
            )
        except kubernetes.client.rest.ApiException:
            self.k8s_core_v1.create_namespaced_config_map(
                namespace="default",
                body=configmap
            )