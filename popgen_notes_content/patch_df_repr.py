import great_tables


def patch_repr(df):
    def ltx():
        temp = great_tables.GT(df).as_latex().split("\n")
        first = None
        last = None
        for i, t in enumerate(temp):
            if t.find("tabular") != -1:
                if first is None:
                    first = i
                else:
                    last = i + 1
                    break
        temp = "\n".join(temp[first:last])
        temp += "\n"
        return temp

    def html():
        return great_tables.GT(df).as_raw_html()

    df._repr_latex_ = ltx
    df._repr_html_ = html
    return df
