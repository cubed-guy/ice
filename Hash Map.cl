#[1024](33, 4, ^5)hash_map:
	*4__getitem__(self, 33key):
		4index = hash(key)
		*(33, 4, ^5)node = self[index]
		while node[0] != key: node = node[2]
		return node[1]
