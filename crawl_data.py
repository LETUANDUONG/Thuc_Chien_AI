import requests
from bs4 import BeautifulSoup
import pandas as pd 

def crawl_techcombank_highlights(url):
    """
    Crawl dữ liệu bảng highlights từ trang Techcombank.
    Args:
        url (str): URL của trang web cần crawl.
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu bảng, hoặc None nếu có lỗi.
    """
    try:
        # Gửi yêu cầu HTTP để lấy nội dung trang
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra các lỗi HTTP (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy dữ liệu từ URL: {e}")
        return None

    # Phân tích cú pháp HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm div chứa bảng (quan sát từ Developer Tools)
    # Thử tìm theo ID 'highlights' trước, sau đó tìm div chứa bảng
    highlights_section = soup.find('div', id='highlights')
    financial_info_div = None

    if highlights_section:
        financial_info_div = highlights_section.find('div', class_='statistics-table-container')
    
    if not financial_info_div:
        # Nếu không tìm thấy trong section highlights, thử tìm trực tiếp trên toàn trang
        financial_info_div = soup.find('div', class_='statistics-table-container')

    if not financial_info_div:
        print("Không tìm thấy div 'statistics-table-container'. Cấu trúc trang có thể đã thay đổi.")
        return None

    # Tìm bảng trong div đó
    table = financial_info_div.find('table')

    if not table:
        print("Không tìm thấy bảng trong div 'statistics-table-container'. Cấu trúc trang có thể đã thay đổi.")
        return None

    # Trích xuất tiêu đề bảng
    headers = []
    thead = table.find('thead')
    if thead:
        header_row = thead.find('tr')
        if header_row:
            for th in header_row.find_all('th'):
                headers.append(th.get_text(strip=True))
    
    # Fallback: if no thead or headers found, try to get headers from the first row of the table body
    if not headers:
        first_row = table.find('tr') # Find the first row directly under the table
        if first_row:
            for th_or_td in first_row.find_all(['th', 'td']): # Headers can sometimes be in td in the first row
                headers.append(th_or_td.get_text(strip=True))

    # Trích xuất dữ liệu hàng
    data_rows = []
    tbody = table.find('tbody')
    rows_to_process = []

    if tbody:
        rows_to_process = tbody.find_all('tr')
    else:
        # Fallback: if no tbody, get all rows directly under the table,
        # but skip the first row if headers were extracted from it.
        all_rows = table.find_all('tr')
        if headers and all_rows and len(all_rows) > 0 and all_rows[0] == first_row: # If headers were extracted from the first row, skip it
            rows_to_process = all_rows[1:]
        else:
            rows_to_process = all_rows

    for row in rows_to_process:
        cols = row.find_all('td')
        # Lọc bỏ các hàng trống hoặc không phải dữ liệu thực sự
        if cols and len(cols) == len(headers): # Đảm bảo số cột khớp với headers
            row_data = [col.get_text(strip=True) for col in cols]
            data_rows.append(row_data)
        # Bổ sung: Một số hàng có thể có một cột duy nhất là năm, không phải dữ liệu đầy đủ
        elif cols and len(cols) > 1: # Hàng dữ liệu thường có nhiều hơn 1 cột
             row_data = [col.get_text(strip=True) for col in cols]
             data_rows.append(row_data)


    # Tạo DataFrame từ dữ liệu để hiển thị đẹp hơn
    if data_rows:
        # Xử lý trường hợp số lượng cột trong data_rows không khớp với headers
        # Ví dụ: Hàng đầu tiên có thể có nhiều cột hơn, hoặc ít hơn
        # Cố gắng đồng bộ hóa hoặc bỏ qua các hàng không khớp hoàn toàn
        # Ở đây, giả định các hàng data_rows sẽ có số cột tương đồng.
        # Nếu có sự không nhất quán nghiêm trọng, cần logic xử lý phức tạp hơn.
        filtered_data_rows = [row for row in data_rows if len(row) == len(headers)]
        
        # Nếu sau khi lọc vẫn còn dữ liệu
        if filtered_data_rows:
             df = pd.DataFrame(filtered_data_rows, columns=headers)
             return df
        else:
            print("Không có hàng dữ liệu hợp lệ nào được tìm thấy sau khi lọc.")
            return None
    else:
        print("Không có dữ liệu hàng nào được trích xuất.")
        return None

# URL cần crawl
url_to_crawl = "https://techcombank.com/en/investors/financial-information/highlights#highlights"

print(f"Đang crawl dữ liệu từ: {url_to_crawl}")
financial_highlights_df = crawl_techcombank_highlights(url_to_crawl)

if financial_highlights_df is not None:
    print("\nBảng Thông tin Tài chính - Highlights của Techcombank:")
    # In toàn bộ DataFrame, không giới hạn số hàng
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(financial_highlights_df.to_string(index=False)) # to_string(index=False) để không in chỉ mục DataFrame
else:
    print("Không thể thu thập dữ liệu bảng.")
