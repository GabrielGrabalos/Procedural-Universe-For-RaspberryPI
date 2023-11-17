class NameGenerator:

    silables = [
            "a", "e", "i", "o", "u",
            "ba", "be", "bi", "bo", "bu",
            "ca", "ce", "ci", "co", "cu",
            "da", "de", "di", "do", "du",
            "fa", "fe", "fi", "fo", "fu",
            "ga", "ge", "gi", "go", "gu",
            "ja", "je", "ji", "jo", "ju",
            "la", "le", "li", "lo", "lu",
            "ma", "me", "mi", "mo", "mu",
            "na", "ne", "ni", "no", "nu",
            "pa", "pe", "pi", "po", "pu",
            "ra", "re", "ri", "ro", "ru",
            "sa", "se", "si", "so", "su",
            "ta", "te", "ti", "to", "tu",
            "va", "ve", "vi", "vo", "vu",
            "bra", "bre", "bri", "bro", "bru",
            "cra", "cre", "cri", "cro", "cru",
            "dra", "dre", "dri", "dro", "dru",
            "fra", "fre", "fri", "fro", "fru",
            "gra", "gre", "gri", "gro", "gru",
            "pra", "pre", "pri", "pro", "pru",
            "qua", "que", "qui", "quo",
            "bra", "bre", "bri", "bro", "bru",
            "cra", "cre", "cri", "cro", "cru",
            "dra", "dre", "dri", "dro", "dru",
            "pra", "pre", "pri", "pro", "pru",
            "fla", "fle", "fli", "flo", "flu",
            "gla", "gle", "gli", "glo", "glu",
            "pla", "ple", "pli", "plo", "plu",
            "cla", "cle", "cli", "clo", "clu",
            "bla", "ble", "bli", "blo", "blu",
            "tra", "tre", "tri", "tro", "tru",
            "gra", "gre", "gri", "gro", "gru",
            "pra", "pre", "pri", "pro", "pru",
            "cha", "che", "chi", "cho", "chu",
            "pla", "ple", "pli", "plo", "plu",
            "bla", "ble", "bli", "blo", "blu",
            "fla", "fle", "fli", "flo", "flu",
            "cla", "cle", "cli", "clo", "clu",
        ]

    def generate(silable_count, star):
        # Generate a name:
        name = ""
        for i in range(silable_count):
            name += NameGenerator.silables[star.randInt(0, len(NameGenerator.silables) - 1)]

        rand_fac = star.randInt(0, 1000)
        if rand_fac < 5:
            name += " da Silva"
        elif rand_fac < 100:
            name += "son"
        elif rand_fac < 250:
            name += "s"
        elif rand_fac < 250:
            name += "r"

        # Turn the first letter into a capital letter:
        name = name[0].upper() + name[1:]

        return name
