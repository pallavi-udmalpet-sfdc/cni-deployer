output "bastion_sg_id" {
  value = "${aws_security_group.bastion.id}"
}

output "nginx_sg_id" {
  value = "${aws_security_group.nginx.id}"
}
