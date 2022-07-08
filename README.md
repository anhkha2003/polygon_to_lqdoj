# polygon_to_lqdoj

Tool được dùng để chuyển đổi các file ở polygon để phù hợp với lqdoj.

Cài đặt:
- Cài python3
- Mở terminal và chạy lệnh `git clone https://github.com/anhkha2003/polygon_to_lqdoj.git` 

Các bước thực hiện:
- Bước 1: Tải package của problem từ polygon
- Bước 2: Copy file .zip đến folder polygon_to_lqdoj
- Bước 3: Đổi nội dung trong file name.txt giống với tên của file package. Ví dụ file package tên là aplusb-3.zip thì gõ aplusb-3 trong file name.txt
- Bước 4: Chạy chương trình bằng lệnh `python3 main.py` bên trong thư mục polygon_to_lqdoj. Nếu up bài của anh Thái thì chạy lệnh `python3 thai.py`
- Bước 5: Chương trình sẽ tạo ra 2 folder là folder unzip của package và folder output. Folder output chứa đề bài và bộ test để upload lên lqdoj
- Bước 6: Nội dung trong file statement-lqdoj.txt là đề bài đã chuyển đổi latex để phù hợp với lqdoj. File tests.zip là bộ test của problem
