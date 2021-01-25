<template>
  <div class="login-wrap">
    <div class="title">
      <h2>TestPlatform</h2>
    </div>
    <div class="ms-login">
      <div class="ms-title">用 户 注 册</div>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="ms-content">
        <el-form-item prop="username" :error="err_username_msg">
          <!-- @focus="err_username_msg=''" -->
          <el-input v-model="ruleForm.username" clearable @focus="clearValidate('username')">
            <el-button slot="prepend" icon="el-icon-user"></el-button>
          </el-input>
        </el-form-item>

        <el-form-item prop="email" :error="err_email_msg">
          <el-input v-model="ruleForm.email" clearable @focus="clearValidate('email')">
            <el-button slot="prepend" icon="el-icon-message"></el-button>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input type="password" v-model="ruleForm.password" @focus="clearValidate('password')">
            <el-button slot="prepend" icon="el-icon-lock"></el-button>
          </el-input>
        </el-form-item>

        <el-form-item prop="password_confirm">
          <el-input
            type="password"
            v-model="ruleForm.password_confirm"
            @keyup.enter.native="submitForm('ruleForm')"
            @focus="clearValidate('password_confirm')"
          >
            <el-button slot="prepend" icon="el-icon-lock"></el-button>
          </el-input>
        </el-form-item>

        <el-link type="info" :underline="false" class="register_link" href="/login">已有账号？点击登录</el-link>

        <div class="login-btn">
          <el-button type="primary" @click="submitForm('ruleForm')">注册</el-button>
        </div>
        <p class="login-tips" v-show="err_info">{{ err_msg }}</p>
      </el-form>
    </div>
  </div>
</template>

<script>
import { register, check_username, check_email } from "../../api/api";

export default {
  data: function() {
    let validateUsername = (rule, value, callback) => {
      let len = value.length;
      this.err_username_msg = "";
      if (len < 6 || len > 20) {
        callback(new Error("用户名最少4位，最多20位"));
      } else {
        check_username(value)
          .then(response => {
            // console.log('账号数:' + response.data.count)
            if (response.data.count > 0) {
              this.err_username_msg = "用户名已存在";
            } else {
              callback();
            }
          })
          .catch(error => {
            if (error.response) {
              this.err_username_msg = "服务器错误";
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            } else if (error.request) {
              this.err_username_msg = error.request;
              console.log(error.request);
            } else {
              this.err_username_msg = error.message;
              console.log("Error", error.message);
            }
          });
      }
    };

    let validateEmail = (rule, value, callback) => {
      this.err_email_msg = "";
      var re = /^(([^<>()\]\\.,;:\s@"]+(\.[^<>()\]\\.,;:\s@"]+)*)|(".+"))@(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      var result = re.test(value.toLowerCase());
      if (!result) {
        callback(new Error("请输入合法的邮箱地址"));
      } else {
        check_email(value)
          .then(response => {
            if (response.data.count > 0) {
              this.err_email_msg = "邮箱已存在";
            } else {
              callback();
            }
          })
          .catch(error => {
            if (error.response) {
              this.err_email_msg = "服务器错误";
              console.log(error.response.data);
              console.log(error.response.status);
              console.log(error.response.headers);
            } else if (error.request) {
              this.err_email_msg = error.request;
              console.log(error.request);
            } else {
              this.err_email_msg = error.message;
              console.log("Error", error.message);
            }
          });
      }
    };

    let validatePass = (rule, value, callback) => {
      var len = value.length;
      if (len < 6 || len > 20) {
        callback(new Error("密码最少6位，最多20位"));
      } else {
        if (this.ruleForm.password_confirm !== "") {
          this.$refs.ruleForm.validateField("password_confirm");
        }
        callback();
      }
    };

    let validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入确认密码"));
      } else if (value !== this.ruleForm.password) {
        callback(new Error("两次输入的密码不一致"));
      } else {
        callback();
      }
    };

    return {
      ruleForm: {
        username: "",
        email: "",
        password: "",
        password_confirm: ""
      },
      err_info: false, // 是否显示错误提示
      err_msg: "", // 具体错误提示
      err_username_msg: "", // 用户名校验失败的提示信息
      err_email_msg: "", // 邮箱校验失败的提示信息

      rules: {
        username: [{ validator: validateUsername, trigger: "blur" }],
        email: [{ validator: validateEmail, trigger: "blur" }],
        password: [{ validator: validatePass, trigger: "blur" }],
        password_confirm: [{ validator: validatePass2, trigger: "blur" }]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          register(this.ruleForm)
            .then(response => {
              // 记录用户的登录状态
              sessionStorage.clear();
              localStorage.clear();

              localStorage.token = response.data.token;
              localStorage.username = response.data.username;
              localStorage.user_id = response.data.id;
              // console.log(localStorage);

              // 路由跳转
              this.$router.push({ name: "index" });
            })
            .catch(error => {
              if ("non_field_errors" in error && error.status_code === 400) {
                this.err_msg = "用户名或密码错误";
              }

              if (error.response) {
                this.err_msg = "服务器异常";
              } else if (error.request) {
                this.err_msg = "网络异常";
              }
              this.err_info = true;
            });
        } else {
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
  color: #e4e7ed;
  border-bottom: 1px solid #ddd;
}
.ms-login {
  position: absolute;
  width: 500px;
  height: 380px;
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
  padding-left: 35%;
  /* color: #E4E7ED; */
  padding-bottom: 20px;
}
.remember_me >>> .el-form-item__label {
  /* color: #409EFF; */
  color: #e4e7ed;
}
</style>