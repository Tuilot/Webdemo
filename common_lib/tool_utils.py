
def get_pagination(current_page, page_count):  # 显示首两个页码、最后两个页码、当前页码以及当前页码前后各三个页码
    if page_count <= 0:
        page_count = 1
    is_first_page = False
    is_last_page = False
    if current_page > page_count:
        current_page = page_count
    if current_page < 1:
        current_page = 1

    if current_page == 1:
        is_first_page = True
    if current_page == page_count:
        is_last_page = True

    # 首两个页码
    pages = [1]
    if page_count > 1:
        pages.append(2)

    # 是否有折叠页码
    if current_page - 3 > 3:
        pages.append('...')

    for i in range(current_page - 3, current_page + 4):
        if i < 1:
            continue

        if i > page_count:
            break

        if not pages.__contains__(i):
            pages.append(i)

    if current_page + 3 < page_count - 2:
        pages.append('...')

    if (not pages.__contains__(page_count - 1)) and page_count > 1:
        pages.append(page_count - 1)
    if not pages.__contains__(page_count):
        pages.append(page_count)
    data = {
        'is_first_page': is_first_page,
        'is_last_page': is_last_page,
        'page_count': page_count,
        'pagination': pages,
        'current_page': current_page
    }
    return data