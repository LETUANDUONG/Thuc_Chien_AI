# Bài dự thi: Báo cáo Hội đồng Quản trị – Techcombank 2025 Insights

## Giới thiệu dự án

Dự án này được thực hiện với mục tiêu xây dựng một bản báo cáo chuyên nghiệp và sáng tạo dành cho Hội đồng Quản trị của Techcombank. Báo cáo tập trung vào việc tóm tắt kết quả hoạt động tài chính nửa đầu năm 2025, so sánh với cùng kỳ năm 2024, và đưa ra những khuyến nghị chiến lược, cùng triển vọng cho năm 2026.

Sản phẩm cuối cùng là nội dung chi tiết cho một tài liệu in (Booklet) khổ A4, được thiết kế để vừa trình bày hiệu quả trên màn hình lớn, vừa dễ đọc cho các thành viên HĐQT.

## Cấu trúc thư mục và các tệp tin

Dự án bao gồm các tệp tin chính sau:

1.  **`crawl_data.py`**:
    *   **Mục đích**: Đây là một script Python được sử dụng để tự động thu thập (crawl) dữ liệu tài chính công khai từ trang web của Techcombank.
    *   **Công nghệ**: Script ban đầu sử dụng thư viện `requests` và `BeautifulSoup`. Sau đó, nó được nâng cấp để sử dụng `Selenium` và `webdriver-manager` nhằm tương tác với các thành phần động (dynamic elements) trên trang web, chẳng hạn như dropdown chọn năm, để lấy được dữ liệu chính xác nhất.
    *   **Kết quả**: Script này trích xuất các bảng dữ liệu tài chính và là nguồn đầu vào cho việc phân tích.

2.  **`Bao_cao_HDQT_TCB_2025.md`**:
    *   **Mục đích**: Đây là tệp chứa toàn bộ nội dung và cấu trúc của bản báo cáo cuối cùng. Nó được viết dưới định dạng Markdown để dễ dàng chỉnh sửa và chuyển đổi sang các định dạng khác (như PDF).
    *   **Nội dung**: Tệp này bao gồm:
        *   **Lời mở đầu**: Giới thiệu bối cảnh và mục tiêu của báo cáo.
        *   **Tóm tắt kết quả tài chính**: Trình bày 3-5 điểm nhấn tài chính quan trọng nhất của 6 tháng đầu năm 2025, so sánh với 2024.
        *   **Phân tích và nhận định**: Rút ra các "insights" quan trọng từ dữ liệu, làm nổi bật cơ hội và rủi ro.
        *   **Đề xuất chiến lược cho 2026**: Gợi ý 3 lĩnh vực trọng tâm mà Techcombank nên ưu tiên, kèm theo lý giải.
        *   **Gợi ý trực quan hóa**: Đề xuất các loại biểu đồ và hình ảnh để minh họa cho từng phần, giúp câu chuyện dữ liệu trở nên sống động và dễ hiểu.

## Quá trình thực hiện

1.  **Thu thập dữ liệu**: Ban đầu, dự án tiếp cận bằng cách crawl dữ liệu tĩnh. Tuy nhiên, sau khi phát hiện dữ liệu được tải động, giải pháp đã được chuyển sang sử dụng Selenium để mô phỏng hành vi người dùng, chọn đúng năm tài chính và lấy dữ liệu cập nhật.
2.  **Phân tích và tổng hợp**: Dữ liệu thu thập được sau đó được phân tích để xác định các xu hướng tăng trưởng, các điểm mạnh và các lĩnh vực cần cải thiện.
3.  **Xây dựng báo cáo**: Dựa trên phân tích, nội dung báo cáo được soạn thảo bằng tiếng Việt, tuân thủ các yêu cầu về một văn bản chuyên nghiệp, súc tích và mang tính chiến lược.
4.  **Sáng tạo và trực quan hóa**: Báo cáo không chỉ dừng lại ở con số mà còn đề xuất các ý tưởng để trình bày dữ liệu một cách trực quan, sáng tạo, phù hợp với yêu cầu của một sản phẩm dành cho cấp lãnh đạo cao nhất.

## Hướng phát triển tiếp theo

- **Tự động hóa hoàn toàn**: Xây dựng một pipeline tự động chạy script `crawl_data.py` định kỳ, phân tích dữ liệu và cập nhật các con số trong báo cáo.
- **Tạo file PDF tự động**: Tích hợp một thư viện (ví dụ: `WeasyPrint` trong Python) để tự động chuyển đổi tệp `Bao_cao_HDQT_TCB_2025.md` thành một file PDF được thiết kế chuyên nghiệp.
- **Dashboard tương tác**: Xây dựng một dashboard trực tuyến (sử dụng các công cụ như Power BI, Tableau hoặc Dash) để HĐQT có thể tương tác trực tiếp với dữ liệu.
