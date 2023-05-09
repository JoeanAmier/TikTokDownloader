def main():
    get_key = ("passport_csrf_token", "odin_tt")
    data = {}
    cookie = input("粘贴 Cookie 后回车：")
    for i in cookie.split('; '):
        text = i.split("=", 1)
        data[text[0]] = text[1]
    result = "; ".join(f"{i}={data.get(i, '')}" for i in get_key)
    print(result)


if __name__ == '__main__':
    main()
