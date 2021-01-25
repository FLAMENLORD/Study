<template>
  <div class="login-wrap">
    <div class="title">
      <h2>TestPlatform</h2>
    </div>
    <div class="ms-login">
      <div class="ms-title">用 户 登 录</div>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="ms-content">
        <el-form-item prop="username">
          <el-input v-model="ruleForm.username" @focus="clearValidate('username')">
            <el-button slot="prepend" icon="el-icon-user"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            v-model="ruleForm.password"
            @keyup.enter.native="submitForm('ruleForm')"
            @focus="clearValidate('password')"
          >
            <el-button slot="prepend" icon="el-icon-lock"></el-button>
          </el-input>
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>

        <el-form-item label="记住我" class="remember_me" size="mini">
          <el-switch v-model="ruleForm.remember_me"></el-switch>
          <el-link type="info" :underline="false" class="register_link" href="/register">没有账号？点击注册</el-link>
        </el-form-item>

        <div class="login-btn">
          <el-button type="primary" @click="submitForm('ruleForm')">登录</el-button>
        </div>
        <p class="login-tips" v-show="err_info">{{ err_msg }}</p>
      </el-form>
    </div>
  </div>
</template>

<script>
import { login } from "../../api/api";

export default {
  data: function() {
    return {
      ruleForm: {
        username: "",
        password: "",
        remember_me: false
      },
      err_info: false,
      err_msg: "",
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        // alert("valid: " + valid);
        if (valid) {
          // localStorage.setItem('ms_username',this.ruleForm.username);
          // this.$router.push('/');
          var that = this;
          login(this.ruleForm)
            .then(response => {
              // 使用浏览器本地存储保存token
              if (that.remember_me) {
                // 记住登录
                sessionStorage.clear();
                localStorage.token = response.data.token;
                localStorage.user_id = response.data.user_id;
                localStorage.username = response.data.username;
              } else {
                // 未记住登录
                localStorage.clear();
                sessionStorage.token = response.data.token;
                sessionStorage.user_id = response.data.user_id;
                sessionStorage.username = response.data.username;
              }

              that.$router.push({ name: "index" });
            })
            .catch(error => {
              console.log(error);
              // if("non_field_errors" in error && error.status_code === 400) {
              if ("non_field_errors" in error) {
                // that.err_msg = error.non_field_errors[0];
                that.err_msg = "用户名或密码错误";
              }

              if (error.response) {
                that.err_msg = "服务器异常";
              } else if (error.request) {
                // that.err_msg = error.message;
                that.err_msg = "网络异常";
              }
              that.err_info = true;
            });
        } else {
          // console.log('error submit!!');
          this.err_msg = "参数有误";
          this.err_info = true;
          return false;
        }
      });
    },
    clearValidate(prop_value) {
      this.$refs["ruleForm"].clearValidate(prop_value);
    }
  }
};
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: #2b4b6b;
  background-size: 100%;
}
.title {
  position: absolute;
  left: 50%;
  top: 15%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #fff;
  font-size: 25px;
  opacity: 0.8;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 25px;
  /* color: rgb(43, 155, 33); */
  color: #fff;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  width: 500px;
  height: 320px;
  left: 50%;
  top: 55%;
  transform: translate(-50%, -50%);
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.3);
  overflow: hidden;
}
.ms-content {
  padding: 30px 30px;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
.login-tips {
  font-size: 12px;
  line-height: 30px;
  color: #f56c6c;
}
.register_link {
  padding-left: 49%;
  color: #d0d1d2;
}
.remember_me >>> .el-form-item__label {
  /* color: #409EFF; */
  color: #e4e7ed;
}
</style>
