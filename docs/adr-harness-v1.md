# Harness v1 · Quyết định kiến trúc

Accepted ghi nhận ràng buộc đã chốt trong thiết kế nguồn. Trạng thái này không cấp quyền thực thi, merge hay bật Bot. Xem [kiến trúc](arc42-harness-v1.md#arc-9) và [hợp đồng kỹ thuật](rfc-harness-v1-detail.md#c-layout).

<a id="adr-001"></a>

## ADR-001. Một vòng đời cho ba profile M2

**Status:** Accepted

### Bối cảnh
Một wizard Repo và một wizard Bot sẽ cùng giữ role, scope và quyền. Khi hai nguồn bất đồng, caller không biết bản nào có thẩm quyền.

### Quyết định
Dùng một cặp Setup/Evolve và một luồng Implement. Tách profile đích `repo-only`, `bot-only`, `repo-and-bot` khỏi mode `interactive` và `persistent-bot`. Không thêm `harness-bot-setup`. Setup chạy hai lượt theo cây. Evolve chỉ xử lý delta trên nền có sẵn, không cài lại và không ghi trong observe/advice.

### Hệ quả
`repo-only` không hỏi Bot. `bot-only` không dựng repo hoặc tracker giả. Hai profile có Bot chọn một hay nhiều `bot_id` rõ ràng; mỗi Bot và đích Repo giữ binding, revision, grant và receipt riêng. Từ chối một đích không hoàn tác đích khác. Mode persistent không suy ra wake. [ADR-015](#adr-015) quy định cách ly nhiều Bot.

### Cơ chế kiểm tra
[Schema M2 và binding](rfc-harness-v1-detail.md#c-profile), [hai lượt Setup](arc42-harness-v1.md#arc-6) và pilot B8. TLC kiểm `SetupReadOnly`, `SetupExplicit`, `ObserveNoWrite`, `IndependentTargets`.

<a id="adr-002"></a>

## ADR-002. Tách tracker Harness và Product

**Status:** Accepted

### Bối cảnh
Hai bộ lọc trên cùng issue set không cách ly công việc Harness với Product. Tracker lỗi cũng không cấp quyền chọn đích thay thế.

### Quyết định
Bind tracker Harness theo instance, namespace, vai trò và quyền đã xác minh. Có thể cùng provider với Product chỉ khi cách ly thực. Product issue chỉ được trỏ ref đọc. Với small-work, chọn record Harness cục bộ bền có instance, namespace, role và grant thật của chính record.

### Hệ quả
Không publish Harness vào Product, Inbox hoặc board điều phối. Không fallback sang record cục bộ sau lỗi tracker. Kiểm split approval đúng draft trước publish và đọc lại ticket canonical tại đích đã chọn.

### Cơ chế kiểm tra
[F9](rfc-harness-v1-detail.md#f9) và [fixture local Harness](rfc-harness-v1-detail.md#c-refs). Kiểm sai role, revision split cũ và local payload hợp lệ bằng checker giữ nguyên. TLC `HarnessOnly` và `SplitApproval`.

<a id="adr-003"></a>

## ADR-003. Dùng mattpocock/skills và khóa chuỗi approval

**Status:** Accepted

### Bối cảnh
Discovery cần methods gốc; phương thức user-only và ví dụ nháp không thể biến thành quyền thực thi.

### Quyết định
Xác minh `grilling`, `domain-modeling` trước node cần dùng. Xác minh `writing-for-agents` và originals `to-spec`, `to-tickets`, `implement` trước authoring. Không vendor; không tự gọi `grill-with-docs`, `wayfinder` hoặc original user-only. Chỉ Apply với grant install H3 mới cài. H4 riêng cho đăng ký ba override project-local. Kiểm exact ID/source/revision, caller, policy và output. Xem [danh mục sáu prerequisite và ba override](arc42-harness-v1.md#skill-inventory). Dùng upstream `handoff` với refs có ACL; nếu không gọi được, nêu đúng bước bàn giao thay vì giả thành công.

### Hệ quả
Hai route ví dụ chỉ soạn nháp. `DesignReady` không duyệt spec. `to-tickets` cần đúng spec revision, basis, scope và evidence approval trước khi chạy. Chỉ soạn artifact còn thiếu; người duyệt lại khi material hoặc basis đổi. Split approval H6 không thay spec approval H5 hoặc publish grant H7. Không thêm envelope handoff thứ bảy.

### Cơ chế kiểm tra
[F5–F8](rfc-harness-v1-detail.md#f5), [routing và ma trận reuse](rfc-harness-v1-detail.md#c-matt), [B7b](rfc-harness-v1-detail.md#rfc-003). Kiểm root/edge của prerequisite, ba override, spec và handoff. TLC `SetupOriginals`, `ThreeOverrides`, `SpecApproval`, `NoUserOnly`.

<a id="adr-004"></a>

## ADR-004. Khảo sát chỉ đọc trước khi đề xuất

**Status:** Accepted

### Bối cảnh
Lời gọi skill không có yêu cầu rõ chưa cấp intent hoặc quyền tạo công việc.

### Quyết định
Sáu entry và mọi `*-discovery` đi thẳng nếu intent rõ. Nếu không, khảo sát thầm trong ACL, chỉ đọc. Setup và topic chỉ dùng intent và facts tĩnh. Lượt đầu khoảng 60 từ, tối đa 8 dòng, có 1–2 đề xuất tác động cao nếu đủ bằng chứng. Đưa bằng chứng đã xác minh trong ngoặc, không chèn việc vệ sinh code; chỉ dẫn link kết nối khi có căn cứ. Dùng đúng title cộng “Something else”, chọn nhiều khi phù hợp, hoặc cùng nhãn inline.

### Hệ quả
Không hỏi trước khảo sát; không ghi hay tạo tác động, kể cả WAL/SHM, trước lựa chọn. Không tạo Inbox card thay chooser. Không có bằng chứng thì không offer. Từ chối, im lặng hoặc sửa chưa rõ không mở request. Chọn tại H1 hoặc đi thẳng vẫn cần exact grant trước mọi write.

### Cơ chế kiểm tra
[F10](rfc-harness-v1-detail.md#f10), [F11](rfc-harness-v1-detail.md#f11) và trace live B8. TLC `ProposalReadOnly`, `ProposalNoEarlyAsk`, `ProposalNeedsPick`, `ProposalNeedsGrant` kiểm thứ tự, không chấm lời đề xuất hay UI.

<a id="adr-005"></a>

## ADR-005. Library năm trạng thái và grant tại kho đích

**Status:** Accepted

### Bối cảnh
SQLite `mode=ro` vẫn có thể tạo WAL/SHM. Exit 0 và digest DB không đổi không chứng minh không ghi hoặc đúng identity.

### Quyết định
Phân biệt `unconfigured`, `missing`, `unreadable`, `wrong-identity` và `ready`. Raw catalog chỉ khi xác nhận unconfigured; revision 0 chỉ ở ready không có row. Mọi read thật dùng cùng no-write preflight; WAL chưa qualify phải chặn trước open, kể cả race mà route không chứng minh được an toàn. Pin đúng catalog và nội dung liên kết của consumer. Cấp hoặc revoke tại H10; kiểm CAS và tiêu thụ grant theo exact bytes, ID, operation, expiry, revision tại SQLite đích. Consume trong cùng transaction với history.

### Hệ quả
Không dùng `immutable=1` trên DB live, không sửa schema. Issue stale hoặc invalid giữ token cũ. Revoke đích trước commit thắng; sau commit không undo. Kho legacy chưa guard không đủ điều kiện chạy nền; token không ra ngoài cơ chế kín. Selection không phải adoption. Rename chỉ carry-forward sau xác minh lineage, owner, scope, revision và readback.

### Cơ chế kiểm tra
[F1](rfc-harness-v1-detail.md#f1), [F2](rfc-harness-v1-detail.md#f2), [schema Library](rfc-harness-v1-detail.md#c-library), [CLI](rfc-harness-v1-detail.md#c-cli). Kiểm đủ sáu đọc, sidecar, bytes, stale issue, revoke, rollback, contention và consume. TLC `NoSidecar`, `NoStaleGrantIssue`, `LibraryCommitCAS`, `GrantSingleUse`.

<a id="adr-006"></a>

## ADR-006. Inbox theo revision, Memory theo ACL

**Status:** Accepted

### Bối cảnh
Reply cũ có thể chốt nhầm ask mới. Kho Memory đã bind bị mất không có nghĩa là Bot không có quy tắc.

### Quyết định
Opt-in Inbox và Memory theo từng `bot_id` và ACL riêng. Ở H11, Inbox khớp authenticated actor, active card, subject, revision, exact action và thread đã gắn với ask của đúng Bot. Thread không chọn Bot và reply không wake hoặc mint grant. Đổi ACL Memory cần chủ có thẩm quyền H12. Đổi material thì supersede. Một ask và một delivery logic có receipt riêng. Memory chỉ ghi từ nguồn trực tiếp hoặc promotion được duyệt, giữ provenance, một batch CAS/sync, rồi worker mới của đúng Bot đọc lại.

### Hệ quả
Tách quyền upsert, send, close và effect; PR terminal thuộc provider. Không đóng lần hai khi native đã settle. Configured missing là Blocked; chỉ tự dùng quy tắc `high` đúng scope, còn hiệu lực và không tranh chấp. `low` chỉ là candidate. Giữ bản gốc và nháp khi conflict; không sync secret, task state, private transcript hoặc bản forward.

Devin Inbox/Needs you có thể dùng board ticket làm biểu diễn thẻ, nhưng không sở hữu trạng thái Tasks/PR. Phiên con dùng Inbox của Bot đã tạo phiên. Không dựa vào dedupe liên Bot. Devin Tasks giữ assignee và session claim riêng; việc Bot quản lý board không chứng minh ACL private. [Seam Devin](rfc-harness-v1-detail.md#devin-tasks-inbox) mô tả các kiểm tra tại đích.

### Cơ chế kiểm tra
[F3](rfc-harness-v1-detail.md#f3), [F4](rfc-harness-v1-detail.md#f4), [keys, trạng thái và ACL](rfc-harness-v1-detail.md#c-errors). Kiểm wrong actor/thread/revision, replay, missing khác empty, stale CAS và fresh-worker readback. TLC `InboxRevision`, `NoReplyGrant`, `MemoryNotEmpty`.

<a id="adr-007"></a>

## ADR-007. Một adapter contract cho bốn host

**Status:** Accepted

### Bối cảnh
Devin, Pi, Claude Code và Codex có cơ chế nạp skill, tool, worker và scheduler khác nhau. Cùng digest ở project khác không chứng minh đúng caller.

### Quyết định
Dùng cùng hợp đồng sáu capability, nhưng binding thuộc đúng đích và mỗi adapter chỉ bind một route thực theo capability. Verify exact ID, source, revision hoặc digest, caller, project, scope, quyền và precedence, kèm `bot_id`/instance khi capability thuộc Bot. Chọn một cách đăng ký trên mỗi host. Inbox và Memory không shadow native. Mỗi fallback phải được chọn và kiểm riêng; không fallback sang Bot khác.

### Hệ quả
Thiếu hoặc mơ hồ primitive không được gọi như đã qualify. Dùng đường chỉ đọc, thủ công được duyệt hoặc giữ tắt theo capability. Không dùng sandbox, native confirmation hoặc cài package thay grant đích hoặc wake.

### Cơ chế kiểm tra
[Ma trận host](arc42-harness-v1.md#arc-7), [B7a và 24 mappings](rfc-harness-v1-detail.md#rfc-002), [B8](rfc-harness-v1-detail.md#rfc-005). TLC `SourceIdentity`, `NoUserOnly`; live bắt foreign digest, wrong caller, shadow và quyền thật.

<a id="adr-008"></a>

## ADR-008. Cổng cấu trúc /correct

**Status:** Accepted

### Bối cảnh
Keyword còn trong prose không chứng minh rule còn đúng. Cần kiểm cạnh vì caller có thể bỏ predecessor dù link vẫn hợp lệ.

### Quyết định
Một owner cho mỗi gate. Mỗi owner có một block `v1-gates` chứa JSON list object đóng `{id,requires}` tạo DAG. Caller link đúng owner, mọi `*-discovery/SKILL.md` được dò tự động. Nhánh thay thế có leaf riêng, không coi OR là AND. GitHub Actions chạy structural test và seam no-write của F1; không tạo runtime Markdown parser.

### Hệ quả
Edge/link mất phải làm check đỏ. Owner cấu hình required check. Không coi CI hoặc lint là bằng chứng host tuân thủ, và không bypass gate khi chưa cấu hình.

### Cơ chế kiểm tra
[Danh sách owner, root, edge và mutant](rfc-harness-v1-detail.md#c-correct), [F11](rfc-harness-v1-detail.md#f11). Kiểm từng cạnh bằng mutant ngoài branch review, baseline xanh, workflow quyền contents read, không secret, không `pull_request_target`. B8 kiểm native riêng.

<a id="adr-009"></a>

## ADR-009. Một chủ mỗi trạng thái và sáu envelope v1

**Status:** Accepted

### Bối cảnh
Bản render, bản sao và checkpoint có thể lệch trạng thái canonical. Checker v1 chỉ kiểm shape, không cấp quyền.

### Quyết định
Mỗi trạng thái có một chủ theo đúng đích, như [bảng ownership](arc42-harness-v1.md#arc-8). Sáu envelope không thêm field. `bots[]` và mapping automation nằm ngoài envelope; mỗi `bot-setup` vẫn chỉ một instance sau config readback và resolve về đúng Bot. Giữ schema, checker, fixture và semantic gate cho envelope legacy. Caller resolve refs và ACL ở scope của mình; đích kiểm revision, claim và grant. Glossary Harness tách Product, ADR giữ lý do, map chỉ trỏ ref.

### Hệ quả
Consumer không ghi dựa vào projection. Không nhúng token, transcript, spec hoặc ticket nguyên bản. Shape đúng mà ref không mở được thì giữ draft hoặc chặn nhánh phụ thuộc. Lưu checkpoint ở nơi có quyền, nếu không giữ inline.

### Cơ chế kiểm tra
[Envelope và mã thoát checker](rfc-harness-v1-detail.md#c-envelope), [ref nghiệp vụ](rfc-harness-v1-detail.md#c-refs), [F8](rfc-harness-v1-detail.md#f8) và [F9](rfc-harness-v1-detail.md#f9). Kiểm `TypeOk` trong TLC; authority và ACL phải kiểm ở đích thật.

<a id="adr-010"></a>

## ADR-010. Áp dụng, đối soát và đóng là ba cổng riêng

**Status:** Accepted

### Bối cảnh
Timeout có thể xảy ra sau commit. Gửi lại, đổi worker hoặc rollback khi chưa biết kết quả có thể lặp tác động.

### Quyết định
`DispatchReady` là dữ kiện live, không phải field bền. Kiểm exact grant, revision và assignment tại đích cho mỗi effect. Thiếu fence bắt buộc thì dừng. Non-atomic chỉ khi policy cho phép và người có quyền xem đúng payload rồi xác nhận từng lần gửi, không chạy nền. `Unknown` chỉ đối soát đích gốc theo stable ID. Không retry, reassign, rollback hoặc close khi chưa có kết luận.

### Hệ quả
Tách receipt ở đích, verify theo đúng tiêu chí và quyền close hoặc writeback. Không advance checkpoint hiệu ứng trong Unknown. Proven no-write mới xét gửi bằng grant mới. Không suy quyền Git, publish, merge hoặc deploy từ quyền execute khác.

### Cơ chế kiểm tra
[Bảng trạng thái, reconcile và đường lỗi](rfc-harness-v1-detail.md#c-errors). B8 thử timeout sau commit và revoke sau last read. TLC `RevocationFence`, `NoWorkReplay`, `VerifyAndClose`.

<a id="adr-011"></a>

## ADR-011. Bật từng trigger và drain trước rebind

**Status:** Accepted

### Bối cảnh
Bot đã cấu hình, chạy tay, resume đạt và trigger active là các kết quả khác nhau. Replay và chuyển host có thể để hai binding cùng thao tác cho một `bot_id`.

### Quyết định
Đọc riêng selection role và contract của từng Bot. Setup hoặc Evolve cấu hình Bot mới bằng grant H19, đọc lại mọi trigger của Bot vẫn tắt. H15 cho phép pilot trên đúng binding và effect; kiểm chạy tay, worker mới đúng ACL và claim/dedupe atomic trước ACK. Chỉ H16 cho phép gửi bật đúng trigger; Agent đọc lại đúng trigger đó. Khi rebind, tắt các trigger của đúng Bot ở binding cũ, đọc lại, drain/fence và đối soát Unknown. Owner duyệt binding mới tại H14. Đọc lại vẫn tắt; qualify lại trên binding mới trước H16.

### Hệ quả
Thiếu primitive thì giữ trigger tắt; operator có thể resume tay qua đường được phép, không qua runner. Không có hai binding active cho cùng `bot_id`. Không chuyển secret, token, transcript hay lịch và không sửa Bot kế bên. Duyệt B8 ở H18 không cấp quyền H15 hoặc H16.

### Cơ chế kiểm tra
[B7c](rfc-harness-v1-detail.md#rfc-004), [B8](rfc-harness-v1-detail.md#rfc-005) và [bảng kiểm nhiều Bot](rfc-harness-v1-detail.md#multi-bot-verification) khóa các cổng theo Bot và binding. Các kết quả TLC lịch sử như `WakeOnce`, `TriggerIsolation` và `DrainBeforeRebind` chỉ kiểm lát một Bot.

<a id="adr-012"></a>

## ADR-012. Phân kỳ PR và kiểm chứng trước phát hành

**Status:** Accepted

### Bối cảnh
Sửa cổng, đăng ký, ví dụ và pilot cần evidence khác nhau. TLC và CLI không thể thay bằng chứng native.

### Quyết định
Landing theo thứ tự Fix-Now F1–F11, B7a, B7b, B7c và B8. Cạnh dependency không đồng nghĩa thứ tự merge. Mỗi PR có whitelist và ô unit, live, perf. [Tiêu chuẩn bốn nhóm tài nguyên](rfc-harness-v1-detail.md#resource-standards) và [runbook hàng đợi](rfc-harness-v1-detail.md#queue-runbook) áp dụng trong cả dây. Dồn docs hướng dẫn và mọi README vào B8. B8 có Prototype bằng route thật bốn host, blind Eval tất cả `SKILL.md`, ReadMe Generation, /technical-writing, /unslop và owner review H18.

### Hệ quả
Pin baseline theo PR. H20 yêu cầu owner cho go trước dây và review PR đổi hành vi, tương tác hoặc host trước merge. Không nhận native nếu thiếu điều kiện mà owner chưa cho defer. Eval phát hiện lỗi chặn pilot thì sửa ở PR riêng được duyệt, không trộn vào PR docs. Không coi review là grant hiệu ứng.

### Cơ chế kiểm tra
[Đồ thị](rfc-harness-v1-detail.md#dependency), [cổng chung](rfc-harness-v1-detail.md#gates) và [gói owner review B8](rfc-harness-v1-detail.md#rfc-005). Đối chiếu [bằng chứng đã có](arc42-harness-v1.md#arc-10) với [phần chưa qualify](arc42-harness-v1.md#arc-11).

<a id="adr-013"></a>

## ADR-013. Tách discovery theo node và giữ ba override ngoài entry mặc định

**Status:** Proposed, chờ owner duyệt gói thiết kế.

### Bối cảnh
Một checklist dài trong Setup buộc nạp nhiều hướng dẫn dù chỉ mở một node. Đăng ký mọi sub-skill và override làm mặc định cũng tăng prompt và cho caller sai đọc route.

### Quyết định
Giữ bốn entry mặc định và hai opt-in. Tách bảy branch chủ và bốn topic con thành 11 file riêng trong [danh mục chuẩn](arc42-harness-v1.md#skill-inventory). Setup điều phối hai lượt và các checkpoint. Mỗi handler chỉ lo một node, dùng upstream method và Library đúng pin, và trả kết quả cho Setup. Nạp on-demand theo exact ID/source/caller. Ba override có file source riêng, đăng ký project-local khi được cấp H4, giữ upstream ID và policy.

### Hệ quả
Không biến CLI/MCP, roles hoặc Software Factory thành entry mới; nhánh cha giữ các chủ đề đó. Tiêu chí readiness cho override không làm native route tự bật. Authoring và budget kiểm ở F6/F10, /correct khóa inventory và edges ở F11, B7a chứng minh fixture, B8 chứng minh route thật và blind Eval. Không thêm schema hoặc nơi lưu trạng thái.

### Cơ chế kiểm tra
[F6](rfc-harness-v1-detail.md#f6), [F10](rfc-harness-v1-detail.md#f10), [hợp đồng route](rfc-harness-v1-detail.md#skill-contracts) và [B8](rfc-harness-v1-detail.md#b8-pilot).

<a id="adr-014"></a>

## ADR-014. Một bảng mã Human cho văn bản và sơ đồ

**Status:** Proposed, chờ owner duyệt gói thiết kế.

### Bối cảnh
Biểu diễn phê duyệt, grant và xác nhận như một bước làm mất actor và revision. Hệ quả là dễ hiểu chọn đề xuất hoặc reply Inbox đã cho phép ghi.

### Quyết định
Dùng [bảng cổng H1–H20](arc42-harness-v1.md#human-gates) làm nguồn duy nhất của mã. Đặt ID cạnh hành động Human, không đặt cạnh thao tác thuần Agent. Đích giữ grant, revision, ownership, CAS và receipt; Agent giữ ref và xử lý theo đường lỗi. /correct có DAG riêng, không chạy logic từ mã H.

### Hệ quả
Không tăng số lần hỏi nếu có quyền/decision hiện hành. Xác nhận non-atomic H9 cần Human ở mỗi lần gửi. H13 không quyết định một effect đã xảy ra hay chưa. H18 không cấp quyền pilot, rebind hoặc bật trigger. Recovery diagrams tách race theo authority gốc; không quy đổi TLC cũ thành pass native.

### Cơ chế kiểm tra
[Danh mục sơ đồ](arc42-harness-v1.md#diagram-contract), [đường chuyển và lỗi](rfc-harness-v1-detail.md#c-errors) và [review B8](rfc-harness-v1-detail.md#b8-pilot).

<a id="adr-015"></a>

## ADR-015. Nhiều Bot độc lập, chỉ automation được đánh thức

**Status:** Accepted cho thiết kế v1. Chưa triển khai hoặc qualify native.

### Bối cảnh

Một Harness có thể cần nhiều vai trò Bot. Định tuyến hội thoại hoặc để nhiều Bot cùng tranh một luồng tạo thêm quyền truy cập, trạng thái dùng chung và một chủ xử lý không rõ ràng. Khả năng Devin hỗ trợ kết nối Bot-to-Bot không phải yêu cầu của Harness v1.

### Quyết định

1. Cấu hình `bots[]` theo `bot_id` ổn định. Mỗi Bot có `role`, `contract`, `binding`, `bot-inbox`, `bot-memory`, `grant`, `revision` và `receipt` riêng. Chỉ kho `harness-library` dùng chung; mỗi Bot đọc theo scope và grant của mình.
2. Chỉ automation lịch hoặc sự kiện tích hợp đã duyệt được đánh thức Bot nền. Mỗi `automation_id` trỏ đúng một `target_bot_id` và binding còn hiệu lực. Bot đích claim occurrence và giữ khóa dedupe bền, atomic trước ACK. Delivery lặp không dispatch lại. Không định tuyến theo chat, role, nội dung, @mention, Bot-to-Bot hay claim trên thread. Phiên tương tác, reply Inbox và pilot tay không phải wake.
3. Setup/Evolve thêm Bot theo H19, các trigger tắt. H15 cho phép pilot trên một binding; H16 tách riêng theo trigger. H14 rebind một Bot sau khi tắt trigger, drain/fence và đối soát, rồi đọc lại binding mới vẫn tắt. Không copy quyền, secret hoặc lịch từ Bot khác hoặc binding cũ.

### Hệ quả

Thiếu hoặc lệch target, binding, grant, primitive atomic hay evidence thì không wake. Không dùng Bot mặc định, broadcast, poll hoặc chat thay runner. Không phân xử việc trên chat. Nếu nhiều nguồn cùng nhắc một việc nghiệp vụ, đích đã chọn kiểm canonical `work_id` và work claim, không thay bằng khóa occurrence. Không thêm envelope, scheduler, tracker hay store.

### Cơ chế kiểm tra

- F2–F4 khóa scope Library, Inbox và Memory bằng fixture có hai Bot. F10 chặn chat ở đường wake. F11 khóa predecessor cho exact target, claim/dedupe trước ACK, H19/H15/H16 và drain trước H14.
- B7a phải reject target thiếu, lệch, nhiều đích hoặc binding cũ; thử duplicate đồng thời và crash quanh ACK; chứng minh chat và @mention không có wake. B7c xác nhận hai Bot mới tắt và tác động trên Bot A không đổi Bot B.
- B8 cần bằng chứng route thật trong phạm vi được cấp: chỉ trigger được duyệt đánh thức đúng Bot, replay không dispatch thêm, rebind một Bot không đổi Bot kia. Test phải đỏ khi bỏ exact target, ACK trước claim/dedupe, chấp nhận chat hoặc dùng state Bot khác. Xem [bảng kiểm chứng](rfc-harness-v1-detail.md#multi-bot-verification).
