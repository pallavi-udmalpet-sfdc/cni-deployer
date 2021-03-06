variable image_id {}
variable instance_type {}
variable vpc_id {}
variable subnet_ids {
  type = list(string)
}
variable key_name {}
variable iam_instance_profile {}
variable region {}
variable docker_image_id {}
variable tags {
  type = map(string)
}
variable vpc_security_group_ids {
  type = list(string)
}
variable admin_principals {
  type = list(string)
}
variable resource_prefix {}
variable retention_in_days {}
