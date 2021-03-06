###############################
#  IAM Role
###############################

resource aws_iam_role bastion {
  name = local.bastion_iam_role_name

  permissions_boundary = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/PCSKPermissionsBoundary"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF

  tags = var.tags
}

###############################
#  Instance Profile
###############################

resource aws_iam_instance_profile bastion {
  name_prefix  = local.bastion_iam_role_name
  role         = aws_iam_role.bastion.name
}

###############################
#  Service-Linked Role
###############################

resource aws_iam_service_linked_role bastion_autoscaling_group {
  aws_service_name = "autoscaling.amazonaws.com"
  custom_suffix    = var.resource_prefix
}
