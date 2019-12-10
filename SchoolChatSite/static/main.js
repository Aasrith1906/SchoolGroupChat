
var password = "audhaw;dhapoghefg;hagh[q0ygfw'ptg929]06tu";

function EncryptMessage(string)
{
    var encrypted_message = CryptoJS.AES.encrypt(string , password);

    return encrypted_message;
}

function DecryptMessage(encrypted_message)
{
    var decrypred_message = CryptoJS.AES.decrypt(encrypted_message,password)

    decrypred_message = decrypred_message.toString(CryptoJS.enc.Utf8)
}
var socket = io.connect('http://' + document.domain + ':' + location.port + '/Chat');

        socket.on('Test',function(message)
        {
            console.log(message);
            $('div.message-holder').append('<div><b style="color: #000">'+message.username+'</b> '+message.data+'</div>' )
        })

        socket.on('RecieveUserMessage',
        function(message){
            var message_value_decrypted = DecryptMessage(message['data'])
            $('div.message-holder').append('<div><b><font color = navy >' +message['username'] +'</font></b> '+ ':' + message_value_decrypted +'</div>' )

        })

        $('#submit').click(
            function(e)
            {
                e.preventDefault()
                var message = $('#EnterMessage').val();
                var message_encrypted = EncryptMessage(message)
                console.log(message_encrypted)
                document.getElementById('EnterMessage').value = null
                socket.emit('UserMessage' , message_encrypted);
               
            }
        )
