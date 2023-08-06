#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .renumbers import re_num_list
from .renumberscales import re_number_scale_list
from .redate import re_date_list
from .reid import re_id_list
from .reabb import list_word_abb
from .reoov import format_word, check_oov_word
from .clean_text import clean_line
import re
# from nltk import word_tokenize


def get_re_idx(re_str, src_txt):
    p_list = [
        (re.compile("^(" + re_str + ")\s"), 1),
        (re.compile("\s(" + re_str + ")$"), 1),
        (re.compile("(?=(\s(" + re_str + ")\s))"), 2),
        (re.compile("^(" + re_str + ")$"), 1),
    ]
    dict_result = dict({})
    for (p, idx) in p_list:
        # print(p, idx)
        # print(p, list(p.finditer(src_txt)))
        for m in p.finditer(src_txt):
            dict_result["{}-{}".format(m.start(idx), len(m.group(idx)))] = m.group(idx)
    return dict_result


def extract_word_tag(txt, txt_tag):
    phrases = []
    phrases_tags = []

    current_tag = 'O'
    phrase = []
    for char, char_tag in zip(list(txt), txt_tag):
        if char_tag.split('-')[-1] != current_tag:
            if len(phrase) > 0:
                phrases.append(''.join(phrase))
                phrases_tags.append(current_tag)
            phrase = [char]
            current_tag = char_tag.split('-')[-1]
        else:
            phrase.append(char)
    if len(phrase) > 0:
        phrases.append(''.join(phrase))
        phrases_tags.append(current_tag)

    words, word_tags = [], []
    for w, t in zip(phrases, phrases_tags):
        list_words = w.strip().split()
        words.extend(list_words)
        if t == 'O':
            word_tags.extend(['O'] * len(list_words))
        else:
            word_tags.append('B-{}'.format(t))
            word_tags.extend(['I-{}'.format(t)] * (len(list_words) - 1))

    return words, word_tags


def tagging(txt, debug=False):
    txt = clean_line(txt)
    txt_tag = ['O'] * len(txt)

    # number
    regex_numer = []
    for re_num in re_num_list:
        result = get_re_idx(re_num, txt)
        if len(result) > 0:
            regex_numer.append(result)
    for rel in regex_numer:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            txt_tag[idx] = 'B-number'
            for i in range(idx + 1, idx + len_item):
                txt_tag[i] = 'I-number'
    if debug:
        print(regex_numer)
    # date
    regex_date = []
    for re_date in re_date_list:
        result = get_re_idx(re_date, txt)
        if len(result) > 0:
            regex_date.append(result)

    for rel in regex_date:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            txt_tag[idx] = 'B-date'
            for i in range(idx + 1, idx + len_item):
                txt_tag[i] = 'I-date'
    if debug:
        print(regex_date)
    # number + scale
    regex_numscale = []
    for re_num_scale in re_number_scale_list:
        result = get_re_idx(re_num_scale, txt)
        if len(result) > 0:
            regex_numscale.append(result)
    for rel in regex_numscale:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            txt_tag[idx] = 'B-numscale'
            for i in range(idx + 1, idx + len_item):
                txt_tag[i] = 'I-numscale'
    if debug:
        print(regex_numscale)
    # id
    regex_id = []
    for re_id in re_id_list:
        result = get_re_idx(re_id, txt)
        if len(result) > 0:
            regex_id.append(result)
    if debug:
        print(regex_id)
    for rel in regex_id:
        for pos in rel.keys():
            idx = int(pos.split('-')[0])
            len_item = int(pos.split('-')[1])
            if list(set(txt_tag[idx:idx + len_item])) == ['O']:
                txt_tag[idx] = 'B-id'
                for i in range(idx + 1, idx + len_item):
                    txt_tag[i] = 'I-id'
    # OOV
    chars = []
    word_idx = 0
    oov_words = []
    for idx, char in enumerate(list(txt)):
        if char != ' ':
            chars.append(char)
        else:
            if len(chars) > 0:
                word = ''.join(chars)
                if format_word(word) in list_word_abb:
                    oov_words.append(word)
                    if list(set(txt_tag[word_idx:word_idx + len(chars)])) == ['O']:
                        txt_tag[word_idx] = 'B-abbrev'
                        for i in range(word_idx + 1, word_idx + len(chars)):
                            txt_tag[i] = 'I-abbrev'
                else:
                    # check oov
                    if check_oov_word(word):
                        oov_words.append(word)
                        if list(set(txt_tag[word_idx:word_idx + len(chars)])) == ['O']:
                            txt_tag[word_idx] = 'B-oov'
                            for i in range(word_idx + 1, word_idx + len(chars)):
                                txt_tag[i] = 'I-oov'
            chars = []
            word_idx = idx + 1
    if len(chars) > 0:
        word = ''.join(chars)
        if format_word(word) in list_word_abb:
            oov_words.append(word)
            if list(set(txt_tag[word_idx:word_idx + len(chars)])) == ['O']:
                txt_tag[word_idx] = 'B-abbrev'
                for i in range(word_idx + 1, word_idx + len(chars)):
                    txt_tag[i] = 'I-abbrev'
        else:
            # check oov
            if check_oov_word(word):
                oov_words.append(word)
                if list(set(txt_tag[word_idx:word_idx + len(chars)])) == ['O']:
                    txt_tag[word_idx] = 'B-oov'
                    for i in range(word_idx + 1, word_idx + len(chars)):
                        txt_tag[i] = 'I-oov'

    if debug:
        print(oov_words)
    return extract_word_tag(txt, txt_tag)


if __name__ == "__main__":
    input_text = 'Samsung Display Việt Nam kiến nghị hợp nhất 3 giai đoạn đầu tư  , Bộ Tài chính nói gì  ?  , Bộ Tài chính vừa có báo cáo gửi Thủ tướng Chính phủ về việc Công ty TNHH Samsung Display Việt Nam đề nghị gộp các giai đoạn đầu tư khác thành một dự án duy nhất và được áp dụng một điều kiện hưởng ưu đãi chung cho cả ba giai đoạn.  , Kinh tế  ,  ,2018-02-03T09:48:57  , Vietnam Finance  , Bộ Tài chính đồng ý việc hợp nhất 3 giai đoạn đầu tư thành 1 dự án tổng thể của Samsung Display Việt Nam  . 3 giai đoạn đầu tư của SDV  . Theo Bộ Tài chính  , hoạt động của Công ty TNHH Samsung Display Việt Nam SDV từ tháng 7/2014 đến nay được chia thành 3 giai đoạn  . Giai đoạn 1 là dự án đầu tư mới lần đầu  . Theo đó  , dự án được cấp giấy chứng nhận đăng ký đầu tư vào tháng 7/2014 với tổng vốn 1 tỷ USD  . Công văn 1048/VPCP-QHQT ngày 16/6/2014 của Thủ tướng đã cho phép dự án được hưởng ưu đãi thuế thu nhập doanh nghiệp theo tiêu chí dự án ứng dụng công nghệ cao với thuế suất 10 % trong 30 năm  , miễn thuế 4 năm và giảm 50 % số thuế phải nộp trong 9 năm tiếp theo  . Ngoài ra SDV cũng được hưởng phần ưu đãi bổ sung thêm 3 năm mức giảm 50 % số thuế thu nhập doanh nghiệp do UBND tỉnh Bắc Ninh trình HĐND tỉnh quyết định theo thẩm quyền  . Theo công văn số 06/TTg-QHQT ngày 15/1/2017 của Thủ tướng  , SDV được chuyển sang hưởng ưu đãi theo tiêu chí dự án có quy mô lớn nếu đáp ứng đủ điều kiện về dự án có quy mô vốn tối thiểu 12.000 tỷ đồng cho thời gian còn lại  . Bộ Tài chính cho biết  , SDV đã giải ngân đủ 1 tỷ USD bao gồm 0,27 tỷ USD nhà xưởng và 0,73 tỷ USD thiết bị máy móc trong thời gian từ 7/2014 3/2017  . Doanh thu năm 205 là 2,68 tỷ USD năm 2016 là 4,06 tỷ USD và 10 tháng đầu năm 2017 là 6,27 tỷ USD  . Số lao động đến cuối tháng 10/2017 là 13.734 người  . Giai đoạn 2  , dự án đầu tư mở rộng lần thứ 1  , được cấp phép thực hiện vào tháng 7/2015 với quy mô vốn 3 tỷ USD  . Theo công văn số 970/VPCP-QHQT ngày 15/5/2015  , Thủ tướng đã đồng ý cho dự án hưởng ưu đãi với cơ chế thuế suất 10 % trong 30 năm  , miễn thuế 4 năm và giảm 50 % số thuế phải nộp trong 9 năm tiếp theo  . Việc đề nghị ưu đaĩa bổ sung được hưởng thêm 3 năm mức giảm 50 % số thuế thu nhập doanh nghiệp sẽ do tỉnh Bắc Ninh quyết định  . Theo giấy chứng nhận đăng ký đầu tư  , công suất dự kiến sau khi giải ngân xong là 120 triệu sản phẩm  . Thời gian giải ngân từ tháng 7/2015 đến hết 2017  . Thực tế SDV đã giải ngân đủ 3 tỷ USD gồm 1,04 tỷ USD nhà xưởng và 1,98 tỷ USD thiết bị máy móc  . Doanh thu năm 2016 là 0,47 tỷ USD và 10 tháng đầu năm 2017 là 3,64 tỷ USD  . Số lượng lao động trực tiếp đến tháng 10/2017 là 16.763 người  . Giai đoạn 3  , dự án mở rộng đầu tư lần 3  , bắt đầu từ tháng 2/2017 khi SDV tăng vốn thêm 2,5 tỷ USD  , nâng tổng vốn đầu tư toàn dự án lên 6,5 tỷ USD  . Theo giấy chứng nhận đăng ký đầu tư  , công suất dự kiến sau khi giải ngân xong là 58 triệu sản phẩm  , thời gian giải ngân từ 2018 2022  . Trên thực tế  , SDV đã giải ngân được 1,66 tỷ USD gồm 0,14 tỷ USD nhà xưởng và 1,52 tỷ USD thiết bị  . Doanh thu tính đến tháng 10/2017 là 1,46 tỷ USD  . Số lượng lao động trực tiếp trên các dây chuyền tính đến tháng 10/2017 là 13.344 người  . SDV kiến nghị được hợp nhất 3 giai đoạn  . SDV cho rằng theo quy định của Luật thuế Thu nhập doanh nghiệp về điều kiện hưởng ưu đãi theo dự án đầu tư có quy mô lớn quy mô vốn đầu tư tối thiểu 12.000 tỷ đồng  , sử dụng công nghệ phải được thẩm định theo quy định của Luật công nghệ cao  , Luật khoa học và công nghệ  , thực hiện giải ngân vốn đầu tư đăng ký không quá 5 năm kể từ ngày được phép đầu tư và điều kiện để được kéo dài thêm thời gian hưởng thuế suất ưu đãi 10 % trong 15 năm là doanh thu hàng năm đạt 20.000 tỷ đồng trong vòng 5 năm kể từ năm đầu tiên phát sinh doanh thu  , hoặc sử dụng thường xuyên 6.000 lao đông thì dự án đầu tư ban đầu và các dự án đầu tư mở rộng của công ty đều đáp ứng điều kiện để hưởng ưu đãi theo điều kiện dự án có quy mô lớn  . Theo đó  , hầu hết tiêu chí đặt ra SDV đều đạt  . Công ty cũng cho biết trong quá trình thực hiện  , nếu phải quản lý  , kê khai riêng theo 3 dự án riêng biệt thì công ty gặp phải nhiều khó khăn vướng mắc  . Chẳng hạn như việc phải chia tách nhân lực từ cấp quản lý đến công nhân  , điều này sẽ dẫn đến khó khăn trong chỉ đạo điều hành  , bộ máy quản lý phình to  , không hợp lý  . Hoặc do đặc thù kinh doanh của ngành sản xuất màn hình  , công nghệ mới luôn luôn được cập nhât  , quá trình hoạt động sản xuất luôn cần đầu tư thêm/hủy bỏ hay di chuyển các công đoạn  , dây chuyền sản xuất các dự án có thể sử dụng chung cơ sở vật chất và các hạ tầng tiện ích hỗ trợ mà không phân chia theo từng giai đoạn đầu tư  . Vì vậy việc phân định rõ ràng vốn đầu tư theo từng dây chuyền sản xuất và tách riêng theo vốn đầu tư của từng dự án là một nhiệm vụ rất khó  . Do vậy  , SDV đã đề nghị Chính phủ chấp thuận cho phép toàn bộ số vốn đầu tư 6,5 tỷ USD được coi là một tổng thể  , một dự án đầu tư duy nhất và được áp dụng điều kiện hưởng ưu đãi chung theo tiêu chí quy mô lớn thuế suất 10 % trong 30 năm  , miễn thuế 4 năm và giảm 50 % số thuế phải nộp trong 9 năm liên tiếp theo do đáp ứng được điều kiện quy mô vốn đầu tư tối thiểu là 12.000 tỷ đồng  . Nếu được chấp thuận  , SDV cam kết sẽ hoàn thành giải ngân toàn bô số vốn đầu tư 6,5 tỷ USD trong vòng 5 năm hạn cuối là tháng 6/2019  . Công ty cũng cam kết sau khi hoàn thành giải ngân vốn đầu tư  , doanh thu của SDV sẽ đạt khoảng 21 tỷ USD vào năm 2022  . Hợp nhất 3 dự án không ảnh hưởng đến thu ngân sách  . Trước đề xuất của SDV  , Bộ Tài chính cho rằng về việc phê duyệt hợp nhất 3 dự án đầu tư theo đề xuất của UBND tỉnh Bắc Ninh và SDV UBND tỉnh Bắc Ninh và SDV khẳng định đây là dự án duy nhất do toàn bộ các giai đoạn đầu tư của SDV với tổng mức đầu tư 6,5 tỷ USD được cấp một mã số dự án duy nhất thuộc chức năng của nhiệm vụ của Bộ Kế hoạch và Đầu tư  . Do vậy  , Bộ trình Thủ tướng giao Bộ Kế hoạch và Đầu tư nghiên cứu  , báo cáo Thủ tướng  . Về ưu đãi thuế thu nhập doanh nghiệp  , Bộ Tài chính cho biết qua kiểm tra và số liệu báo cáo của các cơ quan quản lý trực tiếp của tỉnh Bắc Ninh và SDV cung cấp thì từng dự án độc lập của SDV đã đáp ứng điều kiện theo quy định dự án đầu tư có quy mô lớn  , đồng thời việc kê khai chung cho 3 dự án không ảnh hưởng tới số thu ngân sách nhà nước  . Vì vậy  , để tạo điều kiện cho SDV trong quá trình kê khai hưởng ưu đãi thuế  , Bộ Tài chính trình Thủ tướng cho phép SDV được kê khai xác định ưu đãi như 1 dự án thay vì từng dự án riêng  . Cụ thể  , năm 2017 SDV đăng ký chuyển đổi điều kiện hưởng ưu đãi từ dự án ứng dụng công nghệ cao sang dự án có quy mô vốn đầu tư tối thiểu 12.000 tỷ đồng thì SDV được xác định thuế suất ưu đãi tính từ khi có doanh thu cho thời gian ưu đãi còn lại từ kỳ tính thuế năm 2017 và thời gian miễn  , giảm thuế còn lại từ khi có thu nhập chịu thuế từ dự án đầu tư lần đầu  . Bộ Tài chính cũng cho biết  , trong thời gian được hưởng ưu đãi thuế thu nhập doanh nghiệp  , nếu năm nào mà SDV không đáp ứng được một trong các điều kiện để được hưởng ưu đãi thì năm đó không được hưởng ưu đãi thuế thu nhập doanh nghiệp  . Đồng thời  , Bộ Tài chính trình Thủ tướng Chính phủ giao UBND tỉnh Bắc Ninh chỉ đạo Cục thuế tỉnh Bắc Ninh hướng dẫn đơn vị thực hiện theo quy định của pháp luật và hướng dẫn nêu trên  , không làm giảm thu ngân sách nhà nước  . Trước đó  , tại buổi làm việc với UBND tỉnh Bắc Ninh hồi tháng 10/2017  , sau khi nghe tỉnh này kiến nghị về việc chấp thuận gộp các giai đoạn đầu tư khác nhau của Công ty trách nhiệm hữu hạn Samsung Display tại Bắc Ninh thành một dự án duy nhất và được áp dụng một điều kiện hưởng ưu đãi chung cho cả ba giai đoạn nhằm tháo gỡ khó khăn  , vướng mắc  , tạo điều kiện thuận lợi cho công ty trong việc hạch toán và dự báo trong hoạt động sản xuất  , Thủ tướng đã khẳng định quan điểm tạo điều kiện thuận lợi cho Samsung tuy nhiên phải đảm bảo yêu cầu không làm giảm thu ngân sách nhà nước  , hoặc giảm ít  , đồng thời đảm bảo môi trường đầu tư  . Vĩnh Chi  .'
    # input_text = ' '.join(word_tokenize(input_text))
    print(input_text)
    tags = tagging(input_text)
    for p_i in tags:
        print(p_i)
