var exec = require('child_process').exec
const Koa = require('koa')
const views = require('koa-views')
const path = require('path')
const static = require('koa-static')
const app = new Koa()

// 静态资源目录对于相对入口文件weibo_test1.js的路径
const staticPath = './static'
let url
let user_name = 'realDonalTrump'

app.use(static(
    path.join( __dirname,  staticPath)
))

app.use(views(path.join(__dirname, './view'), {
  extension: 'ejs'
}))

app.use( async ( ctx ) => {
  url = ctx.request.url
  let url_split = url.split('/')
  let url_length = url_split.length
  let i
  // console.log(url_split)
  for(i = url_length - 1; i > 0; i--){
    if(url_split[i] != ''){
      user_name = url_split[i]
      // console.log(user_name)
      break
    }
  }
  var myDate = new Date()

  console.log(myDate.toLocaleString(), user_name)

  if(user_name != 'favicon.ico'){
//    exec('python getTwitterData.py '+ user_name +' ',function(error,stdout,stderr){
//      if(stdout.length >1){
//          console.log('you offer args:',stdout);
//      }
//      if(error) {
//          console.info('stderr : '+stderr);
//      }
//    });
  }

  let title = 'hello koa2'
  await ctx.render('test', {
    title,
  })  
})

app.listen(3000, "0.0.0.0", ()=>{
  console.log('The ejs is starting at 3000')})

