#!/usr/bin/env python3

from tld import get_tld
import sys

gen_suffix = "(sorted by sort.py)"
filter_filename = "filters.txt"


def is_comment(line):
    return len(line) >= 1 and line[:1] == "!"


def is_blank(line):
    line = line.strip(" ")
    return line == ""


def is_generated(line):
    return len(line) >= len(gen_suffix) and line[-len(gen_suffix) :] == gen_suffix


# group_by_root_domain takes a list of rules and returns a dict whose keys are the ROOT_DOMAINs
# for rules and whose values are lists of rules each having the key ROOT_DOMAIN.
def group_by_root_domain(rules):
    ans = dict()
    for r in rules:
        root_domain = extract_root_domain(r)
        if root_domain not in ans:
            ans[root_domain] = []
        ans[root_domain].append(r)
    return ans


def extract_root_domain(rule):
    rule = rule.replace("$", "/")
    rule = rule.replace("|", "")
    rule = "http://" + rule
    res = get_tld(rule, as_object=True)
    return res.fld


def main():
    with open(filter_filename) as f:
        data = [x.strip("\n") for x in f.readlines()]

    comments = []
    rules = []

    for l in data:
        if is_blank(l):
            continue
        if is_generated(l):
            continue

        if is_comment(l):
            comments.append(l)
        else:
            rules.append(l)

    per_domain = group_by_root_domain(rules)

    output_lines = []

    output_lines += comments
    output_lines.append("")

    for root_domain in per_domain:
        output_lines.append("! " + root_domain + " " + gen_suffix)
        rules_for_domain = sorted(list(set(per_domain[root_domain])))
        for r in rules_for_domain:
            output_lines.append(r)
        output_lines.append("")

    with open(filter_filename, "w") as f:
        f.write(("\n".join(output_lines)))


if __name__ == "__main__":
    sys.exit(main())
