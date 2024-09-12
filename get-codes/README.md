自动获取 codeforces 上某特定用户的所有代码，以 `<ProblemName>+<ProblemId>+<ProblemRating>+<Author>+<SubmissionId>` 的格式保存于以用户名命名的子文件夹内，用以配合 `add-lens` 脚本。

需要在工作目录下有 cookies.json 记录 codeforces 的 JSESSIONID，在 codeforces 登录后，`f12` -> `applications` -> `cookie` 下可以找到