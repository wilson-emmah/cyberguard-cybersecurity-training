const tokens = await api('/auth/token/', {
  method: 'POST',
  body: JSON.stringify({
    username: form.get('username'),
    password: form.get('password'),
  }),
});

saveTokens(tokens);

router.push('/dashboard');
