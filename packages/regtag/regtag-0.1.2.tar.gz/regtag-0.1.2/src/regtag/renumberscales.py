re_number_scale_list = [
    "\d{1,7}[ ]*",
    "\d{1,7}[\.,]\d{1,7}[ ]*",
    "\d{1,3}[\.,]\d{3}[\.,]\d{1,5}[ ]*",
    "\d{1,3}[\.,]\d{3}[\.,]\d{1,3}[\.,]\d{1,5}[ ]",
]
re_number_scale_list = [item + "(s|h|p|g|kg|mg|hz|m|km|mb|gb|tb|l|m3|m2|km2|km3|kw|w|v|%)" for item in re_number_scale_list]