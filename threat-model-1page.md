# Threat Model - Lab 3

## Thông tin nhóm
- Thành viên 1: Trần Đình Khiêm (1871020334)
- Thành viên 2: La Văn Hải (1871020215)

## Assets
- **DES key (8 byte)** và **IV (8 byte)** dùng để giải mã.
- **Ciphertext** và **plaintext/message** của người dùng.
- Tính **đúng đắn** của quá trình nhận packet (header length) và quá trình **unpad**.
- **Log/minh chứng** chạy hệ thống.

## Attacker model
- Attacker có thể **quan sát/chen ngang (tamper)** dữ liệu trên đường truyền TCP trong mô hình lab (ví dụ: có quyền truy cập mạng nội bộ).
- Attacker có thể **replay** hoặc **đổi nội dung** packet (sửa ciphertext, sai length header, hoặc thay key/IV nếu thấy/giả mạo).
- Attacker có thể không có khả năng phá DES-CBC một cách trực tiếp (do key được tạo ngẫu nhiên), nhưng có thể lợi dụng **thiết kế gửi key/IV plaintext** và **thiếu xác thực toàn vẹn**.

## Threats
1) **Lộ key/IV qua plaintext**: Sender gửi `key + iv` trực tiếp trong packet → kẻ tấn công đọc được key/IV và giải mã được ciphertext.
2) **Tampering ciphertext**: Không có MAC/AEAD → attacker sửa bits trong ciphertext có thể gây lỗi padding hoặc biến đổi plaintext (tuỳ cách receiver xử lý).
3) **Length header manipulation**: Nếu attacker thay đổi length header, receiver có thể đọc sai ranh giới/ciphertext → làm lỗi parsing, treo timeout, hoặc dẫn tới giải mã dữ liệu sai.
4) **Padding oracle (theo hướng thực nghiệm)**: Nếu receiver phản hồi khác nhau rõ rệt khi padding sai, attacker có thể khai thác phân biệt để suy đoán nội dung/giá trị.

## Mitigations
1) **Không gửi key/IV plaintext**: Dùng cơ chế trao đổi khoá an toàn (ví dụ: TLS handshake) hoặc ít nhất dùng key agreement.
2) **Xác thực toàn vẹn**: Thêm **MAC** (HMAC) hoặc dùng mode **AEAD** (GCM/ChaCha20-Poly1305) để phát hiện tampering trước khi giải mã.
3) **Validation chặt chẽ header**: Kiểm tra `length` có hợp lệ (bội số của block size và nằm trong giới hạn) trước khi đọc/giải mã.
4) **Giảm khác biệt lỗi**: Khi unpad/padding sai, trả thông báo/behavior tương tự để hạn chế padding oracle.

## Residual risks
- Dù có xác thực toàn vẹn, nếu hệ thống vẫn dùng DES-CBC (DES yếu, 64-bit block) và thiếu thiết kế hiện đại, vẫn có rủi ro về **tính bảo mật thực dụng** trong bối cảnh ngoài đời.
- Trong lab, việc chạy demo trên mạng nội bộ vẫn có thể bị tấn công replay/DoS mức ứng dụng nếu không có giới hạn kết nối/timeout hợp lý.

