# Create Leetcode File

Reference original ticket, https://github.com/pmpme/etc/issues/1

## To Run

1. Clone repo `git@github.com:pmpme/etc.git`
2. Navigate to target directory `cd etc/1-create-leetcode-file`
3. Either run from directory using `bash leet <PREFIX> <CATEGORY> <LEETCODE_URL>`
4. OR symlink to user bin directory to run from anywhere `ln -s $(pwd)/leet ~/bin/leet` and make executable `chmod +x ~/bin/leet`

## Example Outputs

### Error - Missing arguments

```
❯ leet

🚨 Please try again!
Usage: leet <PREFIX> <CATEGORY> <LEETCODE_URL>
Ex:    leet p001 arraystring https://leetcode.com/problems/merge-sorted-array/

```

### In Debug Mode with hardcoded arguments

```
❯ leet
✅ Created file p001-88-merge-sorted-array--arraystring.py



--- Reference ---
DEBUG=1
URL=https://leetcode.com/problems/merge-sorted-array/?envType=study-plan-v2&envId=top-interview-150
PROBLEM_URL=https://leetcode.com/problems/merge-sorted-array/
PROBLEM_URL=https://leetcode.com/problems/merge-sorted-array/
RESPONSE={"data":{"question":{"questionId":"88","title":"Merge Sorted Array"}}}
PROBLEM_ID=88
URLSLUG=merge-sorted-array
FILEPATH=p001-88-merge-sorted-array--arraystring.py
FILEPATH=p001-88-merge-sorted-array--arraystring.py
```

### Error - File exists

```
❯ leet p001 "Array/String" https://leetcode.com/problems/merge-sorted-array/description/\?envType\=study-plan-v2\&envId\=top-interview-150
⚠️  File p001-88-merge-sorted-array--arraystring.py already exists


```

### Success - File created

```
❯ # --- ending with urlslug, no trailing slash
❯ leet p001 arraystring https://leetcode.com/problems/merge-sorted-array
✅ Created file p001-88-merge-sorted-array--arraystring.py

❯ # --- ending with urlslug, and trailing slash
❯ leet p002 "Array/String" https://leetcode.com/problems/remove-element/
✅ Created file p002-27-remove-element--arraystring.py

❯ # --- full url from study plan
❯ leet p003 ArrayString https://leetcode.com/problems/remove-duplicates-from-sorted-array/\?envType\=study-plan-v2\&envId\=top-interview-150
✅ Created file p003-26-remove-duplicates-from-sorted-array--arraystring.py

❯ ls p00*
p001-88-merge-sorted-array--arraystring.py
p002-27-remove-element--arraystring.py
p003-26-remove-duplicates-from-sorted-array--arraystring.py
/2025-12 main ⇡1 !1 ?3 ❯
```
