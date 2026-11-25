# Harness v1 · Sơ đồ multi-bot và biên Tasks/Inbox

| Sơ đồ | Nguồn | SVG | PNG | HTML độc lập |
| --- | --- | --- | --- | --- |
| C4 | [PUML](harness-kit-v1-c4.puml) | [SVG](https://app.devin.ai/attachments/a1507c4d-e082-4a7a-9d37-604b40f06dd3/harness-kit-v1-c4.svg) | [PNG](harness-kit-v1-c4.png) | [HTML](harness-kit-v1-c4.html) |
| Biên quyền và chủ dữ liệu | [PUML](https://app.devin.ai/attachments/2deb148b-6402-45ad-9d10-1c146ba7d480/harness-kit-v1-permission-boundary.puml) | [SVG](https://app.devin.ai/attachments/dd63f585-d7df-49f1-8289-40e9ebf20cdf/harness-kit-v1-permission-boundary.svg) | [PNG](harness-kit-v1-permission-boundary.png) | [HTML](harness-kit-v1-permission-boundary.html) |
| Recovery Bot | [PUML](https://app.devin.ai/attachments/4b1db70a-8dcf-4f67-a2c3-65b6a7fc2b60/harness-kit-v1-recovery-bot.puml) | [SVG](https://app.devin.ai/attachments/1d44513a-f349-48a3-967c-a28c523d624e/harness-kit-v1-recovery-bot.svg) | [PNG](harness-kit-v1-recovery-bot.png) | [HTML](harness-kit-v1-recovery-bot.html) |

## Stage 2B: cổng Human

| Sơ đồ | Nguồn | PNG | HTML |
| --- | --- | --- | --- |
| Swimlane theo skill | [PUML](v1-per-skill-human-flow.puml) | [PNG](v1-per-skill-human-flow.png) | [HTML](v1-per-skill-human-flow.html) |
| Statechart vị trí Human | [PUML](v1-human-position-statechart.puml) | [PNG](v1-human-position-statechart.png) | [HTML](v1-human-position-statechart.html) |

Đọc [arc42](../arc42-harness-v1.md), [ADR](../adr-harness-v1.md),
[RFC](../rfc-harness-v1-detail.md), [thiết kế multi-Bot](devin-multi-bot-design.md)
và [bằng chứng B8](../harness-v1.md#b8-qualification-evidence). Các liên kết
ngoài repository cần quyền mở tệp đính kèm Devin. Tải HTML về để mở trong
trình duyệt. HTML Stage 2B cần truy cập `static.devin.ai` để tải trình xem;
dùng PNG khi không có mạng.

## Giới hạn của bộ sơ đồ B8

- Bộ tệp đã duyệt chỉ có sơ đồ Recovery Bot. Xem
  [đặc tả Recovery Library và Implement](../arc42-harness-v1.md#diagram-contract)
  cho hai sơ đồ chưa có trong bộ tệp. Cần duyệt riêng trước khi bổ sung.
- Swimlane Implement đi qua H5 khi vẽ liền mạch từ soạn nháp đến thực thi.
  Với yêu cầu `execute` trực tiếp, làm theo
  [DispatchReady](../../skills/harness/harness-implement/WORK.md#dispatch-and-integrate).
  H5 chỉ chặn gọi `to-tickets` khi chuẩn bị, không phải cổng của `execute`.

## Ghi chú từ lần đối chiếu thiết kế

**Boundary Discipline.** Hai automation đi vào hai đích riêng theo target_bot_id. Tasks giữ trạng thái ticket và claim. Inbox của từng Bot giữ ask và disposition, không ghi thay Tasks hay GitHub.

**Make Operations Idempotent.** Recovery vẽ commit claim, khóa dedupe và pending trước ACK. Retry đọc cùng ledger của Bot, không dispatch lại. Rebind giữ khóa cũ và không đổi Bot khác.

**Prove It Works.** Đã đối chiếu H1–H20, danh mục skill và thứ tự recovery với arc42/ADR/RFC đã khóa. Đã xem từng PNG để kiểm chồng/cắt chữ; mở cả ba HTML không cần mạng và kiểm nút xem chữ lớn. Không sửa repository, chưa chạy TLC hay pilot native.
