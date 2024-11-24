# **Tổng quan về demo**

### **Mục đích:**
Demo này cho phép người dùng gửi thông điệp vào Kafka, nhận thông điệp từ Kafka và hiển thị chúng trên giao diện web theo thời gian thực. Đồng thời, người dùng có thể "clear" các thông điệp đã nhận bằng cách nhấn nút **Clear Topic**.

### Các công nghệ sử dụng:
- **Flask**: Framework Python để xây dựng ứng dụng web.
- **Kafka**: Hệ thống message queue dùng để gửi và nhận thông điệp giữa các producer và consumer.
- **WebSocket (qua Flask-SocketIO)**: Để giao tiếp thời gian thực giữa server và client (để nhận thông điệp mới ngay lập tức mà không cần tải lại trang).
- **Docker**: Sử dụng để quản lý Kafka và các dịch vụ của bạn.

### **Cách hoạt động:**

#### **1. Kết nối với Kafka:**
- **Producer** (Flask App) gửi thông điệp tới Kafka topic khi người dùng nhập vào ô nhập liệu và nhấn nút gửi.
- **Consumer** (Flask App) liên tục lắng nghe Kafka topic và nhận các thông điệp mới được gửi vào.

#### **2. WebSocket giữa server và client:**
- Khi **consumer** nhận được thông điệp mới từ Kafka, thông điệp này sẽ được phát qua **WebSocket** tới trình duyệt (client), và client sẽ cập nhật nội dung trên giao diện mà không cần phải tải lại trang.
- **SocketIO** trong Flask giúp thiết lập kết nối WebSocket này, qua đó server có thể gửi thông điệp mới đến client trong thời gian thực.

#### **3. Hiển thị thông điệp:**
- Mỗi thông điệp mới từ Kafka sẽ được **thêm vào bảng** trong giao diện người dùng (HTML).
- Các thông điệp sẽ được hiển thị dưới tiêu đề **"Received Messages"** trong phần bảng (`div#messages`).

#### **4. Clear Topic:**
- Khi người dùng nhấn nút **Clear Topic**, tất cả các thông điệp hiển thị trong bảng sẽ bị **xóa**.
- **Consumer offset** sẽ được **reset**, và các thông điệp đã fetch trước đó sẽ không còn hiển thị nữa.
- Các thông điệp sau đó từ Kafka sẽ lại được hiển thị như là thông điệp mới.