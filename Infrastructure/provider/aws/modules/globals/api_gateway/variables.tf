variable resource_prefix {}
variable tags {
  type = map(string)
}
variable info_inbound_get_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable info_outbound_get_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_inbound_get_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_inbound_get_one_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_inbound_update_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_inbound_delete_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_outbound_get_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_outbound_create_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_outbound_get_one_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_outbound_update_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}
variable privatelinks_outbound_delete_lambda {
  type = object({
    invoke_arn    = string,
    function_name = string
  })
}