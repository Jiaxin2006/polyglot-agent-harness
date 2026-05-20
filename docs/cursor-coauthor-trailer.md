# Cursor `Co-authored-by` trailer

Cursor may append `Co-authored-by: Cursor <cursoragent@cursor.com>` to commit
messages created via `git commit` in the IDE/agent shell, even when the message
uses `-m` / HEREDOC and `pr-workflow` forbids co-author trailers. This repo has
no active `.git/hooks` (only samples) and no project `.cursor/hooks`.

To verify a commit body: `git log -1 --format=%B`.

To create commits without the trailer from automation, use plumbing, e.g. stage
changes then `git commit-tree "$(git write-tree)" -p HEAD -F message.txt` and
`git reset --hard` to the new commit (or commit from a normal terminal outside
Cursor).
