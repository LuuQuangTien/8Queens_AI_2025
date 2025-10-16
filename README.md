# Báo cáo bài tập AI cá nhân

## Giới thiệu
Đây là bài báo cáo bài tập cá nhân về thực hiện giải bài toán 8 con hậu với những thuật toán tìm kiếm đường đi đã được học trong học kỳ 1 năm 2025-2026.

Giảng viên hướng dẫn: Phan Thị Huyền Trang
Sinh viên thực hiện: Lưu Quang Tiến - 23110157

## Mục tiêu
Ứng dụng những nhóm thuật toán để thực hiện bài toán 8 con hậu. Từ đó tìm những thuật toán tối ưu, phù hợp nhất để giải bài toán.

## Mô tả bài toán
* Trạng thái ban đầu (Initial State): Bàn cờ 8x8 rỗng, gồm 64 ô được đánh số theo hàng và cột.
* Trạng thái mục tiêu (Goal State): Cả 8 con hậu được đặt trên bàn cờ sao cho không có con nào có thể tấn công con khác.
* Hành động (Actions): Thực hiện đặt từng con hậu vào các vị trí đảm bảo an toàn.
* Không gian trạng thái (State): Tất cả các trạng thái có thể sinh ra trong quá trình đặt con hậu.

## *Nhóm thuật toán 1*
Ở nhóm thuật toán này, bàn cờ ở bên phải là trạng thái mục tiêu được người dùng đặt sẵn.

### BFS
Thuật toán sẽ quét cạn qua không gian trạng thái cho đến khi tìm được trạng thái mục tiêu. Thứ tự những trạng thái được thực hiện là FILO (First In Last Out) trong hàng đợi.

### DFS
Thuật toán tìm kiếm theo chiều sâu bắt đầu từ trạng thái ban đầu đến trạng thái mục tiêu, Thứ tự những trạng thái được thực hiện là FIFO (First In First Out) trong hàng đợi. DFS có thể tìm kiếm đường đi nhanh hơn BFS với không gian trạng thái nhỏ hơn, nhưng nhược điểm của DFS là nó có thể bị kẹt trong vòng lặp vô tận, không thể đến trạng thái mục tiêu.
