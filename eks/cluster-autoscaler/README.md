# Install Cluster Autoscaler in AWS EKS Cluster

### Steps

1. Add tags to your Auto Scaling Groups with following tags:
   1. k8s.io/cluster-autoscaler/***CLUSTER-NAME***: owned
   2. k8s.io/cluster-autoscaler/enabled: true
2. Create an IAM policy which grants permissions that cluster autoscaler requires to use an IAM role.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "autoscaling:SetDesiredCapacity",
                "autoscaling:TerminateInstanceInAutoScalingGroup"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/k8s.io/cluster-autoscaler/CLUSTER-NAME": "owned"
                }
            }
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeAutoScalingGroups",
                "ec2:DescribeLaunchTemplateVersions",
                "autoscaling:DescribeTags",
                "autoscaling:DescribeLaunchConfigurations",
                "ec2:DescribeInstanceTypes"
            ],
            "Resource": "*"
        }
    ]
}
```
3. Create policy using the above json file
```console
aws iam create-policy \
    --policy-name AmazonEKSClusterAutoscalerPolicy \
    --policy-document file://cluster-autoscaler-policy.json
```
4. Create an IAM Role from console:
   1. Open IAM Section
   2. Click on **Create Role**.
   3. In **Trusted Entity Type**, select **Web Identity**
   4. Select your cluster's OIDC provider URL in **Identity Provider**
   5. For **Audience**, choose sts.amazonaws.com
   6. Click on Next
   7. Choose the **AmazonEKSClusterAutoscalerPolicy**
   8. Gice role a name, e.g.  **AmazonEKSClusterAutoscalerRole**
   9. Click on **Create Role**
5. Deploy the **Cluster Autoscaler**
   1. Download the cluster autoscaler manifest YAML file
   ```console
   curl -O https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml
   ```
   2. Modify YOUR-CLUSTER-NAME with your cluster name
   3. Apply the manifest
   ```console
   kubectl apply -f cluster-autoscaler-autodiscover.yaml
   ```
   4. Annotate the **cluster-autoscaler** service account with **ARN** of the **IAM ROLE** you created
   ```console
   kubectl annotate serviceaccount cluster-autoscaler \
   -n kube-system \
   eks.amazonaws.com/role-arn=arn:aws:iam::ACCOUNT_ID:role/AmazonEKSClusterAutoscalerRole
   ```
   5. Patch the deployment to add the below annotation to cluster autoscaler pod
   ```console
   kubectl patch deployment cluster-autoscaler \
   -n kube-system \
   -p '{"spec":{"template":{"metadata":{"annotations":{"cluster-autoscaler.kubernetes.io/safe-to-evict": "false"}}}}}'
   ```
   6. Edit the cluster autoscaler deployment
   ```console
   kubectl -n kube-system edit deployment.apps/cluster-autoscaler
   ```
   7. Add below 2 commands in container command:
      ```console
      --balance-similar-node-groups
      --skip-nodes-with-system-pods=false
      ```
   8. If you want to update the cluster autoscaler deployment image, run the below command:
   ```console
   kubectl set image deployment cluster-autoscaler \
   -n kube-system \
   cluster-autoscaler=registry.k8s.io/autoscaling/cluster-autoscaler:v1.25.n
   ```

### Notes
1. If you are using Amazon Linux Worker Nodes or Debian, you have to update the **volumeMounts** **mouthPath** to
   ```console
   /etc/ssl/certs/ca-bundle.crt
   ```
