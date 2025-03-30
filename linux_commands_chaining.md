Linux Command Chaining

Sequential Chaining (;)

Run commands one after another, regardless of success/failure of the previous command.

mkdir testdir; cd testdir; touch file.txt


---

Conditional Execution - Success (&&)

Run the next command only if the previous command succeeds.

mkdir logs && cd logs && touch error.log


---

Conditional Execution - Failure (||)

Run the next command only if the previous command fails.

pgrep nginx || echo "nginx is not running"


---

Conditional Execution - Success (&&) and Failure (||)

Run the next command on success, or another on failure.

gcc app.c && echo "Build success" || echo "Build failed"


---

Pipeline (|)

Pass the output of one command as input to another.

ps aux | grep nginx | awk '{print $2}'


---

Redirection (>, >>)

Redirect command output to a file.

>: Overwrite

>>: Append


dmesg | grep error >> system_errors.log
