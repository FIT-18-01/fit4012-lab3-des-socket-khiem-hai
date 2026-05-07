# Report 1 page - Lab 3

## Thông tin nhóm
- Thành viên 1: Trần Đình Khiêm (1871020334)
- Thành viên 2: La Văn Hải (1871020215)

## Mục tiêu
- Hiểu luồng gửi/nhận qua TCP socket giữa Sender và Receiver.
- Triển khai mã hoá DES-CBC với IV 8 byte và padding PKCS#7.
- Đóng gói gói tin theo thứ tự: key (8) + IV (8) + length header (4) + ciphertext.
- Kiểm thử luồng xử lý đúng kích thước header/ciphertext và xử lý sai dữ liệu.
- Viết threat model và ghi nhận các hạn chế bảo mật của thiết kế trong lab.

## Phân công thực hiện
- Trần Đình Khiêm: Sender (tạo key/IV, mã hoá DES-CBC, build packet, gửi socket) + hỗ trợ tài liệu/test.
- La Văn Hải: Receiver (lắng nghe, nhận packet theo header, giải mã, in kết quả/log) + phần threat model/ethics.
- Làm chung: viết/duyệt test (roundtrip + padding/header + negative tamper/wrong key), hoàn thiện README và log minh chứng cho CI.

## Cách làm
- `des_socket_utils.py`: cài đặt pad/unpad PKCS#7; encrypt/decrypt DES-CBC; build_packet/parse_header; recv_exact để nhận đủ số byte theo length.
- `sender.py`: lấy MESSAGE từ biến môi trường `MESSAGE` (hoặc input), tạo key/IV ngẫu nhiên, mã hoá, build packet và `sendall` qua TCP.
- `receiver.py`: lắng nghe TCP, nhận đúng `HEADER_SIZE`, parse key/IV/length, nhận đủ ciphertext theo `length`, rồi decrypt và decode UTF-8 để hiển thị.
- Kiểm thử bằng `tests/`: gồm test hợp đồng sender/receiver local và negative test (tamper ciphertext, sai key).

## Kết quả
- Hệ thống thực hiện round-trip thành công: Receiver giải mã ra đúng plaintext đã gửi.
- Các test đảm bảo contract gói tin hoạt động (header length/ciphertext bội số 8) và padding hợp lệ/không hợp lệ.
- Negative tests:
  - `tamper` làm sai ciphertext → giải mã/padding thất bại theo kỳ vọng.
  - `wrong key` → kết quả giải mã không đúng và/hoặc padding không hợp lệ theo kỳ vọng.
- Đã tạo log chạy thật trong `logs/` để làm minh chứng khi demo.

## Kết luận
- Về kỹ thuật: hiểu rõ cách đóng gói/dỡ gói gói tin qua TCP, cách padding PKCS#7 và yêu cầu kích thước cho DES-CBC.
- Về bảo mật: nhận ra việc gửi key/IV plaintext trên cùng kênh TCP là điểm yếu nghiêm trọng, cần cải tiến bằng cơ chế trao đổi khoá an toàn và xác thực toàn vẹn.
- Bài lab giúp rèn tư duy threat model và kiểm thử âm để phát hiện sai lệch/vi phạm giả định.
