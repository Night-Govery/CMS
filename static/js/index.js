var Index = {
	vars: {
		lowin: document.querySelector('.lowin'),
		lowin_brand: document.querySelector('.lowin-brand'),
		lowin_wrapper: document.querySelector('.lowin-wrapper'),
		lowin_login: document.querySelector('.lowin-login'),
		lowin_wrapper_height: 0,
		login_back_link: document.querySelector('.login-back-link'),
		forgot_link: document.querySelector('.forgot-link'),
		login_link: document.querySelector('.login-link'),
		login_btn: document.querySelector('.login-btn'),
		register_link: document.querySelector('.register-link'),
		password_group: document.querySelector('.password-group'),
		password_group_height: 0,
		lowin_register: document.querySelector('.lowin-register'),
		lowin_footer: document.querySelector('.lowin-footer'),
		box: document.getElementsByClassName('lowin-box'),
		option: {}
	},
	register(e) {
		Index.vars.lowin_login.className += ' lowin-animated';
		setTimeout(() => {
			Index.vars.lowin_login.style.display = 'none';
		}, 500);
		Index.vars.lowin_register.style.display = 'block';
		Index.vars.lowin_register.className += ' lowin-animated-flip';

		Index.setHeight(Index.vars.lowin_register.offsetHeight + Index.vars.lowin_footer.offsetHeight);

		e.preventDefault();
	},
	login(e) {
		Index.vars.lowin_register.classList.remove('lowin-animated-flip');
		Index.vars.lowin_register.className += ' lowin-animated-flipback';
		Index.vars.lowin_login.style.display = 'block';
		Index.vars.lowin_login.classList.remove('lowin-animated');
		Index.vars.lowin_login.className += ' lowin-animatedback';
		setTimeout(() => {
			Index.vars.lowin_register.style.display = 'none';
		}, 500);
		
		setTimeout(() => {
			Index.vars.lowin_register.classList.remove('lowin-animated-flipback');
			Index.vars.lowin_login.classList.remove('lowin-animatedback');
		},1000);

		Index.setHeight(Index.vars.lowin_login.offsetHeight + Index.vars.lowin_footer.offsetHeight);

		e.preventDefault();
	},
	forgot(e) {
		Index.vars.password_group.classList += ' lowin-animated';
		Index.vars.login_back_link.style.display = 'block';

		setTimeout(() => {
			Index.vars.login_back_link.style.opacity = 1;
			Index.vars.password_group.style.height = 0;
			Index.vars.password_group.style.margin = 0;
		}, 100);
		
		Index.vars.login_btn.innerText = 'Forgot Password';

		Index.setHeight(Index.vars.lowin_wrapper_height - Index.vars.password_group_height);
		Index.vars.lowin_login.querySelector('form').setAttribute('action', Index.vars.option.forgot_url);

		e.preventDefault();
	},
	loginback(e) {
		Index.vars.password_group.classList.remove('lowin-animated');
		Index.vars.password_group.classList += ' lowin-animated-back';
		Index.vars.password_group.style.display = 'block';

		setTimeout(() => {
			Index.vars.login_back_link.style.opacity = 0;
			Index.vars.password_group.style.height = Index.vars.password_group_height + 'px';
			Index.vars.password_group.style.marginBottom = 30 + 'px';
		}, 100);

		setTimeout(() => {
			Index.vars.login_back_link.style.display = 'none';
			Index.vars.password_group.classList.remove('lowin-animated-back');
		}, 1000);

		Index.vars.login_btn.innerText = 'Sign In';
		Index.vars.lowin_login.querySelector('form').setAttribute('action', Index.vars.option.login_url);

		Index.setHeight(Index.vars.lowin_wrapper_height);
		
		e.preventDefault();
	},
	setHeight(height) {
		Index.vars.lowin_wrapper.style.minHeight = height + 'px';
	},
	brand() {
		Index.vars.lowin_brand.classList += ' lowin-animated';
		setTimeout(() => {
			Index.vars.lowin_brand.classList.remove('lowin-animated');
		}, 1000);
	},
	init(option) {
		Index.setHeight(Index.vars.box[0].offsetHeight + Index.vars.lowin_footer.offsetHeight);

		Index.vars.password_group.style.height = Index.vars.password_group.offsetHeight + 'px';
		Index.vars.password_group_height = Index.vars.password_group.offsetHeight;
		Index.vars.lowin_wrapper_height = Index.vars.lowin_wrapper.offsetHeight;

		Index.vars.option = option;
		Index.vars.lowin_login.querySelector('form').setAttribute('action', option.login_url);

		var len = Index.vars.box.length - 1;

		for(var i = 0; i <= len; i++) {
			if(i !== 0) {
				Index.vars.box[i].className += ' lowin-flip';
			}
		}

		Index.vars.forgot_link.addEventListener("click", (e) => {
			Index.forgot(e);
		});

		Index.vars.register_link.addEventListener("click", (e) => {
			Index.brand();
			Index.register(e);
		});

		Index.vars.login_link.addEventListener("click", (e) => {
			Index.brand();
			Index.login(e);
		});

		Index.vars.login_back_link.addEventListener("click", (e) => {
			Index.loginback(e);
		});
	}
}