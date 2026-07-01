# PHẦN BÀI LÀM: SÁNG TẠO - TÍNH NĂNG NGỪNG KINH DOANH SẢN PHẨM

## 1. Luồng dữ liệu (Data Flow)

Khi client gửi request `DELETE /products/{product_id}` lên server, hệ thống sẽ chạy theo các bước sau:

1. **Tiếp nhận:** Router của FastAPI nhận request và bóc tách cái `product_id` từ đường dẫn (URL).
2. **Tìm kiếm:** Hệ thống dùng vòng lặp duyệt qua danh sách `products` đang lưu trong bộ nhớ để dò xem có sản phẩm nào mang cái `id` khớp với `product_id` client gửi lên không.
3. **Xử lý tình huống (Phân luồng logic):**
   - **Nhánh 1 (Không tìm thấy):** Lặp hết mảng mà không có ID nào trùng, hệ thống quăng luôn lỗi HTTP 404 với báo cáo `{"detail": "Product not found"}`. Kết thúc luồng.
   - **Nhánh 2 (Tìm thấy nhưng đã ngừng bán):** Nếu tìm ra sản phẩm, hệ thống check tiếp biến `is_active`. Nếu `is_active` đang là `False` (tức là đã ngừng kinh doanh từ trước rồi), quăng lỗi HTTP 400 kèm thông báo `{"detail": "Product already inactive"}`. Kết thúc luồng.
   - **Nhánh 3 (Trường hợp lý tưởng):** Sản phẩm tồn tại và `is_active` đang là `True`. Hệ thống sẽ gán lại `is_active = False` cho sản phẩm đó.
4. **Trả kết quả:** Server trả về HTTP status 200 kèm một câu thông báo thành công và toàn bộ thông tin của sản phẩm vừa bị đổi trạng thái để client xác nhận.
