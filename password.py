password = 'a123456'
i = 3
while i > 0 :
	i = i - 1
	code = input('請輸入密碼: ')
	if code == password :
		print('登入成功!!')
		break
	else:
		print('密碼錯誤!')
		if i > 0:
			print('你還有 ', i, ' 次機會!!')
		else:
			print('已鎖帳號並報警!!')