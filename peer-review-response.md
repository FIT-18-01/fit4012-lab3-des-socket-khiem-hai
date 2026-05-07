# Peer Review Response

## Thông tin nhóm
- Thành viên 1: Trần Đình Khiêm (1871020334)
- Thành viên 2: La Văn Hải (1871020215)

## Thành viên 1 góp ý cho thành viên 2
Trong vòng lặp nhận dữ liệu qua socket cần đảm bảo đọc đủ số byte theo header length (tránh dùng recv một lần gây thiếu dữ liệu). Đồng thời thống nhất thông điệp/log và đảm bảo giải mã đúng theo thứ tự key + IV + ciphertext.

## Thành viên 2 góp ý cho thành viên 1
Rà soát lại phần pad/unpad PKCS#7 và build/parse packet: unpad phải kiểm tra padding byte-by-byte để negative test (tamper/wrong key) hoạt động đúng kỳ vọng. Bổ sung/đảm bảo tests bao phủ các trường hợp padding/header không hợp lệ.

## Nhóm đã sửa gì sau góp ý
- Bảo đảm `recv_exact` đọc đủ dữ liệu header/ciphertext theo đúng kích thước.
- Kiểm tra padding PKCS#7 chặt chẽ trong `unpad` để test tamper/wrong key phản ứng đúng.
- Hoàn thiện nội dung các file báo cáo (README/report/threat model/peer review) để không còn placeholder chưa điền.
- Tạo log minh chứng chạy thật vào thư mục `logs/` theo checklist CI.


