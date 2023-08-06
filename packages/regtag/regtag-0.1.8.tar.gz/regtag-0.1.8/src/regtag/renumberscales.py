re_number_scale_list = [
    "\d{1,7}[ ]*",
    "\d{1,7}[\.,]\d{1,7}[ ]*",
    "\d{1,7}[\.,\-x]\d{1,7}[ ]*",
    "\d{1,3}[\.,]\d{3}[\.,]\d{1,5}[ ]*",
    "\d{1,3}[\.,]\d{3}[\.,]\d{1,3}[\.,]\d{1,5}[ ]",
]
re_number_scale_list = [item + "(s|h|p|gram|g|kg|mg|hz|cm|mm|m|km|mb|gb|tb|l|m3|m2|ha|km2|km3|kw|w|kWh|kwh|v|%|usd|vnd|đ|euro|cent)" for item in re_number_scale_list]