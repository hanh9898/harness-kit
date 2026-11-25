# Kiến trúc đa Bot của Devin

**Loại:** tài liệu thiết kế tham chiếu và đối chiếu Harness v1 · **Ngày:** 26/11/2026 · **Trạng thái:** để xem xét, không phải đề xuất triển khai đã duyệt.

## 1. Tóm tắt quyết định

**Devin tách Bot lâu dài khỏi phiên làm việc.** Một Bot nhận trách nhiệm về một kết quả, giữ hội thoại, chỉ dẫn, bộ nhớ và quyền truy cập của mình; nó giao từng việc cho phiên con. Nếu nhiều Bot phối hợp, chúng vẫn là các Bot riêng. Chia sẻ Bot hoặc nối Bot A với Bot B là mở quyền trên một Bot đang tồn tại, không phải tạo bản sao và không chỉ là chuyển một tin nhắn.

**Harness v1 đã có nền chạy một Bot:** danh tính host/instance, adapter đã bind, tracker, Inbox, Memory và các cổng vận hành. Hai tài liệu v1 chưa đặc tả **ai sở hữu việc giữa nhiều Bot, quyền nào được mở qua bàn giao, và chặn trùng việc giữa các Bot ở đâu**. Khuyến nghị giữ phạm vi v1; sau khi đủ bằng chứng single-Bot, thử hai Bot với một tuyến bàn giao có hướng, một ticket chính thức và chưa bật trigger.

**Cách đọc:** **Tài liệu Devin** = hành vi được công bố, tra bằng Devin Docs MCP và đọc trang nguồn; **Công cụ Devin** = hợp đồng công cụ hoặc quan sát ở phiên nghiên cứu, không phải cam kết API công khai; **Đề xuất** = thiết kế cho Harness, chưa triển khai. Đây là mô hình logic nhìn từ bên ngoài, không phải sơ đồ backend Cognition.

## 2. Ngữ cảnh và phân ranh

```text
Người dùng / nhóm ── Web, Slack, iMessage ────────────────┐
Lịch / sự kiện tích hợp ── Automation đã cấu hình ────────┤
                                                         v
                              Bot A (trách nhiệm dài hạn)
                     chat + instructions + memory + access
                      │ giao việc                │ hỏi người
                      v                          v
               Tasks / phiên con A1, A2       Needs you / Inbox
                      │                          │
                      └── kết quả về A ──────────┘

Bot A ── quyền đọc/gửi tin A → B ──> Bot B (trách nhiệm và phiên con riêng)
```

**Tài liệu Devin.** Bot là đơn vị nhận **kết quả phải chịu trách nhiệm**; phiên con là đơn vị thực hiện **một phần việc có giới hạn**. Bot theo dõi tiến độ, nhận kết quả hoặc tình huống cần người can thiệp và báo lại. Managed Devins chạy trong VM riêng; quyền dùng kết nối của Bot vẫn áp dụng cho các phiên Bot tạo. **All Bots** là góc nhìn tổng hợp các Bot và phiên mà người dùng có quyền mở, không phải bộ định tuyến hay bảng công việc chung bắt buộc. [D1] [D2] [D3] [D5]

| Thành phần | Phạm vi và quyền đã xác minh |
| --- | --- |
| **Danh tính Bot** | Bot có cấu hình, hội thoại và quyền riêng. Công cụ/runtime phân biệt định danh Bot, phiên và người; phiên này còn hiển thị danh tính service user của Bot. Đó không phải bằng chứng rằng mọi tích hợp xác thực bằng cùng service user: MCP dùng danh tính của tài khoản đăng nhập; PR mặc định do Bot đứng tên, trừ khi người yêu cầu tự bật quyền mở PR dưới tên mình. [D3] [D4] [P1] |
| **Instructions và Memory** | Instructions là cấu hình do người có quyền chỉnh; Memory là tri thức Bot tích lũy, tách khỏi Memory cá nhân và dùng lại qua các phiên. Người có **Can use** đọc được Memory của Bot, kể cả nội dung trước khi được chia sẻ. Công cụ cấp quyền dùng Memory cá nhân là luồng riêng, chỉ khi người đó yêu cầu; không tự trộn hai kho. [D1] [D6] [P2] |
| **Tasks board** | Công cụ phân biệt người được giao ticket với phiên Devin đang claim. `claim`/`dispatch` từ chối ticket còn bị chặn bởi điều kiện phụ thuộc; `dispatch` từ chối ticket đã có claim. Có thể tạo ticket và giao cho phiên con bằng một lệnh. Phiên nghiên cứu thấy board Tasks do Bot quản lý nhưng board có thể mở trong tổ chức: phạm vi vận hành của Bot không đồng nghĩa ACL private của board. [P1] |
| **Inbox / Needs you** | Là nơi tập trung quyết định, quyền, PR cần review/merge và thông tin cần đọc; không phải nguồn trạng thái của ticket công việc hay PR. Công cụ biểu diễn Inbox item dưới dạng board ticket có loại thẻ; phiên con dùng Inbox của Bot đã sinh ra nó. Công cụ có vòng đời Active / On hold / Done / Canceled và theo dõi PR đóng/merge trên GitHub. Không thấy cam kết Inbox tự khử trùng mọi ask giữa nhiều Bot. [D1] [P2] |
| **Connections và secrets** | Bot và các phiên của nó dùng quyền của **Bot**, không đổi sang quyền của người vừa nhắn. Có MCP/plugin/secret riêng của Bot, grant cá nhân có thể thu hồi, và quyền từ phạm vi tổ chức/doanh nghiệp. Tài liệu mô tả thứ tự cho cùng MCP: kết nối/sign-in riêng của Bot → grant của thành viên → kết nối tổ chức/doanh nghiệp. Secret riêng không làm biến mất secret cấp tổ chức mà Bot đã được dùng. [D3] [D4] |
| **Phiên con** | Bot giao việc và có thể nhắn tiếp, nhận thông báo khi phiên con cần input hoặc xong, cho ngủ hoặc dừng. VM riêng cô lập môi trường thực thi, không tự cô lập grant của Bot. Phiên con không trở thành Bot thứ hai chỉ vì có prompt, mode hay repo khác. [D1] [D2] [D3] |

## 3. Vòng đời, chủ sở hữu và chia sẻ

1. **Tạo.** Trong Devin chọn **Create new Bot**, từ template hoặc từ đầu, đặt tên rồi giao mục tiêu. Bot mới mặc định private với người tạo. Một phiên Devin cũng có thể đề xuất tạo Bot; chỉ sau khi người dùng duyệt mới tạo. Theo hợp đồng `devin_bot_create`, người duyệt yêu cầu đó là chủ Bot được tạo. [D1] [P1]
2. **Chia sẻ cùng Bot hoặc chia sẻ mẫu.** Cùng Bot nghĩa là cùng conversation, Memory, connections và các phiên; không dùng cách này để phân phối một prompt. Template truyền chỉ dẫn, không truyền conversation, Memory, kết nối hay secrets. Trước khi share Bot, kiểm **Who can use**, **What it can access**, lịch sử và tài nguyên có thể dùng qua Bot. Với Bot dùng chung, ưu tiên tài khoản dịch vụ riêng cho tích hợp thay vì sign-in cá nhân. [D3] [D4] [D7]
3. **Phân quyền.** **Can use** cho phép nhắn, đọc conversation/Memory/phiên và điều khiển phiên; **Can configure** sửa chỉ dẫn và cấu hình; **Can share** quản lý quyền chia sẻ. Ba quyền không bao hàm nhau. **Manage Bots** có thể share/archive/delete Bot theo phạm vi quản trị nhưng không tự được đọc hội thoại. Grant không vượt người cấp; sign-in mất hiệu lực nếu người cấp mất quyền truy cập tương ứng. Bot private có thể nhận một số tài nguyên sẵn có của chủ không bật hộp thoại, nhưng vẫn ghi grant; Bot shared cần phê duyệt quyền cá nhân mới. Bot private mà một Bot shared dùng được cũng phải hỏi trước khi lấy tài nguyên cá nhân của chủ. [D1] [D3] [D4]
4. **Dừng.** Recycle thay phiên đang chạy của chính Bot; không phải tạo Bot mới. Archive ngừng phản hồi, gỡ app Slack riêng và các liên kết Bot hai chiều; unarchive không tự phục hồi chúng. Delete là vĩnh viễn và xóa cả phiên, Memory, automations và tasks của Bot. Không tìm thấy trong các nguồn đã đọc quy trình chuyển owner hoặc bảo đảm rằng archive chờ mọi thao tác đang chạy kết thúc. Khi thay owner, không suy rằng có thể chuyển nguyên trạng Bot/grant. [D1] [D3]

## 4. Nhiều Bot phối hợp và tránh làm trùng

### 4.1 Hành vi Devin xác nhận

**Grant có hướng.** Cấp A quyền vào B cho phép A đọc B, gồm hội thoại và phiên, và nhắn B; không cho A sửa settings của B hoặc mặc nhiên tạo quyền B → A. Nếu cùng chủ, người tạo chọn B trong **Your Bots** của A (Bot private có thể kết nối Bot private khác cùng chủ khi cần); nếu khác chủ, bên có **Can share** của B thêm A hoặc duyệt yêu cầu của A. Khi một trong hai Bot đã shared, Devin hiển thị xác nhận về quyền/phạm vi hiển thị mở rộng. [D3]

**Quyền đọc và dữ liệu có thể đi qua cạnh.** Người dùng A có thể đọc hoặc nhắn B qua A; người dùng B dùng chung thấy nội dung A gửi vào B. Việc share A sau này không xóa cạnh A → B đã có. Vì vậy, cấp cạnh không phải cơ chế “chỉ gửi ticket”; thu hồi cạnh ở một trong các đầu phù hợp khi không còn cần. [D3]

**Phân vai là mô hình vận hành, không phải bộ định tuyến toàn cục.** Cognition mô tả một Bot điều phối “Super Jenny” gom quyết định từ các Bot chuyên môn về một Slack thread; đây là ví dụ triển khai, không phải cơ chế leader election, định tuyến theo vai trò, khử trùng theo ngữ nghĩa hay bảo đảm xử lý đúng một lần của nền tảng. Devin có hai cơ chế phạm vi hẹp: claim chặn dispatch lại **cùng ticket**; Script Preflight khử trùng item theo ID/phiên bản **trong một automation**, có thể xử lý lại item fail hoặc sau khi xóa state. Hai cơ chế không chứng minh một vấn đề không sinh hai ticket qua các Bot, board hoặc nguồn khác nhau. [D8] [D9] [P1]

### 4.2 Quy tắc điều phối đề xuất cho Harness

| Quy tắc | Cách áp dụng |
| --- | --- |
| **Một bên sở hữu mỗi việc** | Chỉ Bot điều phối nhận yêu cầu và quyết định Bot chuyên môn nào làm; tracker chính thức giữ một ticket, một assignment đang hiệu lực cho công việc. Bên thực hiện không mở ticket/PR thứ hai cho cùng mục tiêu. |
| **Tách hai loại trùng** | `occurrence_key` chặn giao lại **cùng lần phát**; `work_id` tại tracker chặn tạo việc thứ hai qua nhiều nguồn. Dùng ID nghiệp vụ chính thức và revision khi một bản cập nhật thực sự là đơn vị công việc mới. Thiếu phép kiểm atomic cần thiết hoặc không đối soát được thì chỉ phân tuyến thủ công, không chạy nền. |
| **Bàn giao tối thiểu** | Chuyển ticket/ref, scope, revision, tiêu chí nghiệm thu, người nhận và nơi trả kết quả. Bên nhận kiểm lại ACL, claim và grant tại đích; không chuyển token, transcript hoặc xem quyền nhắn như quyền ghi. Dùng đường trả kết quả đã được phép; không tự mở cạnh ngược. |
| **Một nơi hỏi, một nơi báo** | Bot điều phối giữ một ask cho mỗi quyết định, trả lời trong đúng luồng gốc; Bot chuyên môn báo cho điều phối. Không dùng tin Bot đăng làm đầu vào thực thi mặc định; chỉ chấp nhận nguồn handoff đã định danh. Không để cả @mention, webhook và lịch tự giao cùng việc. |

**Ví dụ:** cùng một lỗi đi vào từ Slack và Linear. Điều phối đối chiếu tới cùng issue Linear và dựa trên một `work_id` của **tracker Harness** nếu đó là việc Harness; issue Product chỉ là ref đọc. Điều phối giao đúng một assignment; Bot chuyên môn trả bằng chứng vào đường đã duyệt. Nếu kết quả ghi không rõ (ví dụ mất biên nhận sau khi gửi), giữ `Unknown`, tra đích gốc; không mở ticket, giao lại hoặc gửi lại để “thử”. [H1, §3/§8] [H2, Hợp đồng kỹ thuật]

## 5. Kênh giao tiếp và kích hoạt

| Đường vào | Hành vi và ranh giới Devin |
| --- | --- |
| **Web / Team's Bots** | Chọn đúng Bot từ sidebar; All Bots chỉ hiển thị phạm vi có quyền mở. Việc nhìn thấy nhiều Bot không cấp quyền điều phối hay dùng tài nguyên của chúng. [D1] [D5] |
| **Slack app của Bot** | Nếu chưa cài app riêng, Bot dùng shared Devin app làm fallback. Có app riêng thì có handle riêng, nhận DM hoặc @mention và trả lời trong thread. Tổ chức phải kết nối Slack; creator ủy quyền/cài app, workspace có thể đòi admin duyệt. **Who can message** kiểm DM/người có reply được đọc; **Allowed channels** kiểm tự tham gia, không thay `/invite`. Private channel dùng `/invite`; Bot được thêm vào channel thì có quyền ghi ở đó, không suy quyền ghi từ việc đọc được channel public của shared app. Mở ngoài nhóm share còn phụ thuộc chính sách Slack của tổ chức; mở đến Slack Connect có điều kiện và xác nhận riêng. [D10] |
| **iMessage** | Liên kết số/Apple ID bằng mã một lần, cần **Can use**. Mỗi lần chỉ liên kết một Bot; ngắt Bot cũ trước khi chuyển. Tin nhắn đi vào cùng chat Devin; không có trên Enterprise. Không có mô tả đủ rõ trong hướng dẫn iMessage về group chat, chọn nhiều Bot hoặc dùng tin nhắn để cấp quyền đích; không lấy chúng làm giả định thiết kế. [D11] |
| **Automation** | Khác với DM/@mention. Trigger từ lịch, Slack và các tích hợp đã nối, hoặc webhook; lọc bằng conditions/Preflight rồi mới chạy action. Action có thể mở phiên, nhắn phiên đã chọn hoặc triage, tùy cấu hình; Bot có trang automations riêng. Webhook có secret xác thực; automations có giới hạn nhịp, queue tùy chọn và lịch sử invocation. Admin có thể hạn chế nguồn ngoài Devin; trigger policy không chặn @mention, API/CLI hay schedule nội bộ. Lịch sử run không phải biên nhận effect tại đích. [D1] [D9] |

**Biên tin cậy:** tin nhắn và payload có thể do bên không tin cậy gửi. Quyền nhắn Slack/Bot, có mã liên kết iMessage hoặc có secret webhook chỉ quyết định **đường vào** tương ứng; không dùng chúng như grant cho merge, ghi dữ liệu hay mở quyền mới. Kiểm người gửi, nguồn, scope và quyền tại đích độc lập. Đây là nguyên tắc đề xuất cho Harness, phù hợp với cảnh báo prompt injection của Devin. [D10] [H1, §8]

## 6. Bảng so sánh và khoảng trống của Harness v1

Đối chiếu hai bản thiết kế do chủ cung cấp, baseline nêu trong tài liệu là `main a782f24`. Các mục B7c/B8 là kế hoạch và tiêu chí; không suy từ tài liệu này rằng tính năng đã có trên checkout, adapter đã được nghiệm thu, hay các ca kiểm native đã chạy.

| Mặt | Devin | Harness v1 hiện thiết kế | Khoảng trống / quyết định |
| --- | --- | --- | --- |
| **Danh tính, vai trò, vòng đời** | Bot lâu dài; creator, ACL, template và session là các khái niệm riêng. | `bot_ref`, `owner_ref`, `instance_id`; role và `bot-portable-template` là hai selection riêng. Profile đích khác mode chạy; `bot-setup` chỉ sau config readback. [H1, §2/§8] [H2, RFC-004] | Đủ cho một instance. Chưa có quyền hay vòng đời **giữa** các instance; không thêm Bot registry hoặc giả lập template bằng sao chép state. |
| **Quyền và secrets** | Quyền cạnh A → B mở quyền đọc/nhắn; quyền dùng A có thể tới B qua A. Có kết nối riêng và quyền cấp tổ chức. | Host kiểm caller/ACL; mỗi đích kiểm exact effect/grant/revision; repo và Bot không chung giao dịch; secret store riêng. [H1, §3/§8] | Không ánh xạ `Can use` thành grant ghi. Với cạnh native phải kiểm cả quyền đọc gián tiếp, thu hồi và quyền tổ chức, không chỉ đường gửi. |
| **Tasks, worker, khử trùng** | Board có claim theo ticket; Bot chạy các phiên con; Preflight có dedupe cục bộ. | Tracker Harness tách Product; dedupe `work_id` và node/question/outcome; live assignment/epoch, fence tại đích, đối soát `Unknown`. [H1, §3/§8] [H2, Chuyển trạng thái] | Chưa quy định nhiều Bot phân tuyến tới cùng tracker và chủ công việc giữa các Bot; reuse tracker đã bind, không coi Tasks board/Inbox là tracker Harness thay thế. |
| **Inbox, Memory** | Mỗi Bot có hàng Needs you và Memory; share Bot mở phạm vi người đọc. | Opt-in đúng Bot, Inbox khớp respondent/subject/revision/action/thread và tách delivery receipt; Memory có ACL, provenance, CAS/sync, fresh-worker readback; store đã bind bị mất là Blocked. [H2, F3/F4 và Chuyển trạng thái] | Không cần kho chung. Nếu gom ask qua điều phối, giữ một ask chính thức và chỉ chuyển ref được phép; không sync chéo Memory hoặc coi reply là grant. |
| **Kênh và wake** | Web, Slack app, iMessage và automations có quyền/chính sách riêng; Preflight không khử trùng liên automation. | Adapter cho Devin, Pi, Claude Code, Codex; tách manual → fresh-worker → bật từng trigger; claim/dedupe occurrence trước ACK; drain/fence trước rebind. [H2, RFC-005 và Profile/Chuyển trạng thái] | Chưa có hợp đồng định tuyến và chứng cứ native giữa các Bot/kênh. Không lấy Slack/iMessage hay Preflight làm route portable hoặc bằng chứng về exactly-once/fence. Giữ wake tắt nếu thiếu bằng chứng. |

## 7. Đề xuất quyết định và cổng nghiệm thu

**Đề xuất, không mở rộng v1.** Giữ host là nơi nắm danh tính Bot và quyền kênh, tracker giữ việc/claim, đích giữ grant/receipt, Inbox giữ quyết định và Memory giữ quy tắc. Không thêm scheduler, tracker, store, entry Bot hay envelope thứ bảy. Sau B7c/B8 được cấp quyền và chứng minh đường single-Bot cần thiết, nếu chủ muốn thử multi-Bot, bắt đầu với **hai Bot private, phối hợp thủ công, chỉ đọc**, một chiều A → B nếu quyền đọc rộng của Devin phù hợp; nếu không phù hợp, dùng người điều phối chuyển ref có quyền qua đường hiện có. Không mặc định nối toàn mạng các Bot. Đổi lại, điều phối tập trung có thể nghẽn; lợi ích là một chủ việc, một nơi hỏi người và một dấu vết để đối soát.

| Cổng thử trong môi trường riêng | Dấu hiệu đạt |
| --- | --- |
| **Quyền và chặn rò rỉ** | Người không được cấp không mở được Bot/ref; B không lấy được Memory/secret riêng của A vì nhận handoff; kiểm riêng quyền tổ chức còn hiệu lực. Thu hồi cạnh rồi kiểm truy cập mới bị từ chối. Không suy thu hồi xóa dữ liệu đã gửi. |
| **Bàn giao và khử trùng** | Fixture thử hai đầu vào cùng issue cho một kế hoạch giao việc; chỉ khi có grant riêng mới thử ghi vào tracker cô lập và đo một ticket/assignment, không có PR thứ hai. Reply sai người, thread hoặc revision không chốt ask. Bên nhận không được cấp thêm quyền ghi chỉ vì nhận ref. |
| **Bật automation chỉ khi qua cổng riêng** | Sau manual và fresh-worker readback, chỉ thử đúng một trigger đã duyệt; đọc lại trạng thái thật, thử giao lặp và thiếu biên nhận. `Unknown` giữ checkpoint, không tự retry; dừng có disable/readback và drain/fence theo hợp đồng v1. |

**Chưa xác minh:** không chạy live Slack/iMessage, không tạo/chia sẻ Bot thử và không chạy B8. Không thấy nguồn công khai xác định lưu trữ vật lý per-Bot, hợp đồng giao nhận Bot-to-Bot, chống vòng lặp toàn cục, hoặc khả năng revoke chặn một thao tác đã vượt qua cổng ghi. Những mục này cần chứng cứ tại host/đích, không điền bằng giả định từ sơ đồ.

## Nguồn

| Mã | Tài liệu hoặc bằng chứng |
| --- | --- |
| D1–D2 | [Devin Bots: tổng quan, Needs you, Memory, vòng đời](https://docs.devin.ai/work-with-devin/bots) · [Managed Devins](https://docs.devin.ai/work-with-devin/advanced-capabilities#managed-devins) |
| D3–D4 | [Access and security: ACL, grant, kết nối giữa Bot](https://docs.devin.ai/work-with-devin/bots/access-and-security) · [Connections and secrets](https://docs.devin.ai/work-with-devin/bots/connections) |
| D5–D7 | [All Bots](https://docs.devin.ai/work-with-devin/bots/all-bots) · [Memory and Dreaming](https://docs.devin.ai/product-guides/memory) · [Templates](https://docs.devin.ai/work-with-devin/bots/templates) |
| D8–D9 | [Cognition: ví dụ Super Jenny](https://devin.ai/blog/introducing-devin-bots) · [Automations: trigger, Preflight, limits, safeguards](https://docs.devin.ai/product-guides/automations) |
| D10–D11 | [Slack app của Bot](https://docs.devin.ai/work-with-devin/bots/slack) · [iMessage](https://docs.devin.ai/work-with-devin/bots/imessage) |
| P1 | <a id="p1"></a>Catalog công cụ có trong phiên: `devin_bot_create`, `board_ticket_dispatch`, `devin_ticket_manage`, `devin_board_manage`, `devin_session_create`; quan sát chỉ đọc metadata ticket/board và quan hệ Bot → phiên của phiên nghiên cứu. |
| P2 | <a id="p2"></a>Catalog công cụ `devin_inbox_manage`, `devin_memory_grant_self`; không suy từ mô tả công cụ thành API công khai hay primitive tương đương trên host khác. |
| H1–H2 | [Harness v1 · Kiến trúc arc42](https://app.devin.ai/attachments/10929482-073c-40a8-baea-646ca53a86ed/arc42-harness-v1.md) · [Harness v1 · RFC kỹ thuật](https://app.devin.ai/attachments/4a841ca4-b9cb-4544-87a8-2a12d57bf18b/rfc-harness-v1-detail.md). |

[D1]: https://docs.devin.ai/work-with-devin/bots
[D2]: https://docs.devin.ai/work-with-devin/advanced-capabilities#managed-devins
[D3]: https://docs.devin.ai/work-with-devin/bots/access-and-security
[D4]: https://docs.devin.ai/work-with-devin/bots/connections
[D5]: https://docs.devin.ai/work-with-devin/bots/all-bots
[D6]: https://docs.devin.ai/product-guides/memory
[D7]: https://docs.devin.ai/work-with-devin/bots/templates
[D8]: https://devin.ai/blog/introducing-devin-bots
[D9]: https://docs.devin.ai/product-guides/automations
[D10]: https://docs.devin.ai/work-with-devin/bots/slack
[D11]: https://docs.devin.ai/work-with-devin/bots/imessage
[P1]: #p1
[P2]: #p2
