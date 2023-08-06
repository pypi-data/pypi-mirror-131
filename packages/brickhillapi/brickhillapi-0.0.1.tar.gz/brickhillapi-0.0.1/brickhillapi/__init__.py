from urllib.request import Request, urlopen

def userId(username):
    """Get the ID of a user with their username."""
    getid = Request("https://api.brick-hill.com/v1/user/id?username=" + username, headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("id\":")
    combined = ""
    for i in spl[1]:
        if i.isnumeric():
            combined += i
        else:
            break
    return combined

def name(id):
    """Get the username of a user with their ID."""
    getid = Request("https://api.brick-hill.com/v1/user/profile?id=" + str(id), headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("username\":\"")
    combined = ""
    for i in spl[1]:
        if i != "\"":
            combined += i
        else:
            break
    return combined

def lastOnline(id):
    """Get the last time a user was online."""
    getid = Request("https://api.brick-hill.com/v1/user/profile?id=" + str(id), headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("last_online\":\"")
    combined = ""
    for i in spl[1]:
        if i != "\"":
            combined += i
        else:
            break
    return combined

def created(id):
    """Get the date an account was created."""
    getid = Request("https://api.brick-hill.com/v1/user/profile?id=" + str(id), headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("created_at\":\"")
    combined = ""
    for i in spl[1]:
        if i != "\"":
            combined += i
        else:
            break
    return combined

def description(id):
    """Get the description of a user."""
    getid = Request("https://api.brick-hill.com/v1/user/profile?id=" + str(id), headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("description\":\"")
    combined = ""
    for i in spl[1]:
        if i != "\"":
            combined += i
        else:
            break
    return combined

def awards(id):
    """Get the awards a user has."""
    getid = Request("https://api.brick-hill.com/v1/user/profile?id=" + str(id), headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("awards\":[")
    combined = ""
    awards = ""
    for i in spl[1]:
        if i != "]":
            combined += i
        else:
            break
    spl2 = combined.replace("\n", "").replace(" ", "").split("name\":\"")
    try:
        for i in spl2[1]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[2]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[3]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[4]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[5]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[6]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[7]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    try:
        for i in spl2[8]:
            if i != "\"":
                awards += i
            else:
                break
        awards += ", "
    except:
        pass
    return awards[0:-2]

def updatedItem():
    """Get the last updated item."""
    getid = Request("https://api.brick-hill.com/v1/shop/list?sort=updated&limit=1", headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("id\":")
    combined = ""
    for i in spl[1]:
        if i != ",":
            combined += i
        else:
            break
    return combined

def newestItem():
    """Get the newest item."""
    getid = Request("https://api.brick-hill.com/v1/shop/list?sort=newest&limit=1", headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    spl = str(getidjson).split("id\":")
    combined = ""
    for i in spl[1]:
        if i != ",":
            combined += i
        else:
            break
    return combined

def unreleasedItems(min_id, max_id):
    """Check for unreleased items with an ID between the minimum and maximum."""
    combined = ""
    while min_id <= max_id:
        getid = Request("https://api.brick-hill.com/v1/shop/" + str(min_id), headers={"User-Agent": "Mozilla/5.0"})
        getidjson = urlopen(getid).read()
        spl2 = str(getidjson).split("is_public\":")
        ispublic = ""
        for i in spl2[1]:
            if i != ",":
                ispublic += i
            else:
                break
        if ispublic == "0":
            spl = str(getidjson).split("id\":")
            for i in spl[1]:
                if i != ",":
                    combined += i
                else:
                    break
            combined += ", "
        min_id += 1
    return combined[0:-2]

def avatar(id):
    """Get the avatar of a user."""
    getid = Request("https://api.brick-hill.com/v1/games/retrieveAvatar?id=" + str(id), headers={"User-Agent": "Mozilla/5.0"})
    getidjson = urlopen(getid).read()
    facespl = str(getidjson).split("face\":")
    face = ""
    for i in facespl[1]:
        if i != ",":
            face += i
        else:
            break
    hatsspl = str(getidjson).split("hats\":[")
    hats = ""
    combined = ""
    for i in hatsspl[1]:
        if i != "]":
            combined += i
        else:
            break
    hatsspl2 = combined.replace(" ", "").split("\n")
    for item in hatsspl2:
        for i in item:
            if i != ",":
                hats += i
            else:
                break
        hats += ", "
    hats = hats[0:-2]
    headspl = str(getidjson).split("head\":")
    head = ""
    for i in headspl[1]:
        if i != ",":
            head += i
        else:
            break
    toolspl = str(getidjson).split("tool\":")
    tool = ""
    for i in toolspl[1]:
        if i != ",":
            tool += i
        else:
            break
    pantsspl = str(getidjson).split("pants\":")
    pants = ""
    for i in pantsspl[1]:
        if i != ",":
            pants += i
        else:
            break
    shirtspl = str(getidjson).split("shirt\":")
    shirt = ""
    for i in shirtspl[1]:
        if i != ",":
            shirt += i
        else:
            break
    figurespl = str(getidjson).split("figure\":")
    figure = ""
    for i in figurespl[1]:
        if i != ",":
            figure += i
        else:
            break
    tshirtspl = str(getidjson).split("tshirt\":")
    tshirt = ""
    for i in tshirtspl[1]:
        if i != ",":
            tshirt += i
        else:
            break
    headcolorspl = str(getidjson).split("head\":\"")
    headcolor = ""
    for i in headcolorspl[1]:
        if i != "\"":
            headcolor += i
        else:
            break
    torsocolorspl = str(getidjson).split("torso\":\"")
    torsocolor = ""
    for i in torsocolorspl[1]:
        if i != "\"":
            torsocolor += i
        else:
            break
    lacolorspl = str(getidjson).split("left_arm\":\"")
    lacolor = ""
    for i in lacolorspl[1]:
        if i != "\"":
            lacolor += i
        else:
            break
    llcolorspl = str(getidjson).split("left_leg\":\"")
    llcolor = ""
    for i in llcolorspl[1]:
        if i != "\"":
            llcolor += i
        else:
            break
    racolorspl = str(getidjson).split("right_arm\":\"")
    racolor = ""
    for i in racolorspl[1]:
        if i != "\"":
            racolor += i
        else:
            break
    rlcolorspl = str(getidjson).split("right_leg\":\"")
    rlcolor = ""
    for i in rlcolorspl[1]:
        if i != "\"":
            rlcolor += i
        else:
            break
    return "Hats: " + hats + "\nFace: " + face + "\nTool: " + tool + "\nPants: " + pants + "\nShirt: " + shirt + "\nTshirt: " + tshirt + "\nFigure: " + figure + "\n\nHead color: " + headcolor + "\nTorso color: " + torsocolor + "\nLeft arm color: " + lacolor + "\nLeft leg color: " + llcolor + "\nRight arm color: " + racolor + "\nRight leg color: " + rlcolor

