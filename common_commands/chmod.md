# 🐧 Chmod Reference Guide

The `chmod` (change mode) command defines who can read, write, or execute a file or directory. Permissions are split into three categories: **User (u)**, **Group (g)**, and **Others (o)**.

### BLUF:
1. The Sticky Bit (Prevent Accidental Deletion)
>The Rule: You can create/edit files, but you can only delete your own stuff.
>Best for: Shared "Drop" folders or /tmp.

Commands:
```bash
chmod +t /path/to/dir (Symbolic)
## OR
chmod 1777 /path/to/dir (Numeric)
```

---

### 1. The Numeric Representation
Permissions are calculated by adding the following values:
* **4**: Read (`r`)
* **2**: Write (`w`)
* **1**: Execute (`x`)

| Score | Permission | Description |
| :--- | :--- | :--- |
| **7** | `rwx` | Full access (Read + Write + Execute) |
| **6** | `rw-` | Read and Write |
| **5** | `r-x` | Read and Execute |
| **4** | `r--` | Read only |



---

### 2. Special Permissions (The 4th Digit)
When using a 4-digit command (e.g., `2770`), the first digit represents **Special Bits**.

#### **SetGID (Value: 2)**
Essential for **Team Folders**. When applied to a directory, any new files created inside will inherit the **Group ID** of the parent directory, rather than the primary group of the user who created it.
* **Command:** `chmod 2770 /shared/tech_team`
* **Result:** Ensures everyone in the group can edit new files created by others.

#### **Sticky Bit (Value: 1)**
Used on public directories (like `/tmp`) to prevent users from deleting or renaming files owned by others.
* **Command:** `chmod +t /shared/public_drop` or `chmod 1777 /folder`
* **Result:** Only the file owner or root can delete the file.

#### **SetUID (Value: 4)**
The file executes with the permissions of the **owner** rather than the user running it. 

---

### 3. Common Chmod Commands

| Command | Usage | Description |
| :--- | :--- | :--- |
| `chmod 644` | Files | Owner: RW, Group/Others: R. |
| `chmod 755` | Scripts | Owner: RWX, Group/Others: RX. |
| `chmod 700` | Private | Only the owner has access. |
| **`chmod 2770`** | **Teams** | Owner/Group: Full access + Group Inheritance. |
| `chmod -R` | Recursive | Applies permissions to all sub-files/folders. |

---

### 4. Symbolic vs. Numeric
If you prefer not to do math, you can use symbols:
* `chmod g+s folder/` — Add SetGID to a group.
* `chmod +t folder/` — Add the Sticky Bit.
* `chmod u+x script.sh` — Make a file executable for the owner.
* `chmod o-rwx secret.txt` — Remove all access for "others".

> **Tip:** If you see a lowercase `s` in the group slot (e.g., `rwxr-sr-x`), the SetGID bit is active!