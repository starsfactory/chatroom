   //vue写法
        var vm=new Vue({
            el:"#chat_comment",
            data(){
                return{
                    chat_context_item:null
                }
            },
            methods:{
                commit: fwunction(){
                    var data=new Date();
                    var hour=data.getHours();
                    var mm=data.getMinutes();
                    var time=hour+':'+mm;
                    var ans='<div class="chat_right_item_1 clearfix">热巴</div>'+
                    '<div class="chat_right_item_2">'+
                    '<div class="chat_right_time clearfix">'+time+'</div>'+
                    '<div class="chat_right_content clearfix">'+this.chat_context_item+'</div>'
                    +'</div>';
                    var oLi=document.createElement("div");
                    oLi.setAttribute("class","chat_right");
                    oLi.innerHTML=ans;
                    this.$refs.chat_middle_item.append(oLi);
                    this.chat_context_item=null;
                    let ele = document.getElementById('chat_middle_item');
                    ele.scrollTop = ele.scrollHeight;
                }
            }
        });

