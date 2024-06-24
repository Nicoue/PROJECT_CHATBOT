// Fonction pour ajouter un message à la chatbox
function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const newMessage = document.createElement('div');
    newMessage.classList.add('message', sender);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');

    const img = document.createElement('img');
    if (sender === 'bot') {
        img.src = 'https://png.pngtree.com/png-clipart/20230823/original/pngtree-chatbot-color-icon-chat-bot-picture-image_8213084.png';
        img.alt = 'Bot';
    } else if (sender === 'user') {
        img.src = 'https://www.w3schools.com/w3images/avatar2.png'; 
        img.alt = 'User';
    }

    const messageText = document.createElement('span');
    messageText.textContent = message;

    if (sender === 'user') {
        messageContent.appendChild(messageText);
        messageContent.appendChild(img);
    } else {
        messageContent.appendChild(img);
        messageContent.appendChild(messageText);
    }

    newMessage.appendChild(messageContent);
    chatBox.appendChild(newMessage);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Fonction pour diviser les questions
function splitQuestions(message) {
    return message.split(/[?!.]/).filter(q => q.trim()).map(q => q.trim() + '?');
}

// Fonction pour envoyer un message
async function sendMessage() {
    const input = document.getElementById('user-input');
    const questions = splitQuestions(input.value);
    if (questions.length === 0) {
        console.log('Empty input, ignoring send.');
        return;
    }

    for (const question of questions) {
        appendMessage('user', question);
        await sendSingleQuestion(question);
    }

    input.value = '';
}

// Fonction pour envoyer une question unique avec délai simulé
async function sendSingleQuestion(question) {
    // Affiche un message de chargement du bot
    const loadingMessage = document.createElement('div');
    loadingMessage.classList.add('message', 'bot', 'loading');
    const loadingText = document.createElement('span');
    loadingText.textContent = '...';
    loadingMessage.appendChild(loadingText);
    document.getElementById('chat-box').appendChild(loadingMessage);

    // Simule un délai aléatoire entre 1 et 2 secondes
    const delay = Math.random() * 1000 + 1000;
    await new Promise(resolve => setTimeout(resolve, delay));

    // Supprime le message de chargement
    document.getElementById('chat-box').removeChild(loadingMessage);

    try {
        
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        if (response.ok) {
            const data = await response.json();
            data.response.forEach(message => {
                appendMessage('bot', message);
            });
        } else {
            console.error('Server error:', response.statusText);
            appendMessage('bot', 'Désolé, une erreur est survenue.');
        }
        
    } catch (error) {
        console.error('Fetch error:', error);
        appendMessage('bot', 'Désolé, une erreur est survenue.');
    }
}



// Fonction pour envoyer une réponse rapide
function quickResponse(message) {
    document.getElementById('user-input').value = message;
    sendMessage();
}

// Fonction pour évaluer la réponse
function rateResponse(isPositive) {
    if (isPositive) {
        alert("Merci pour votre avis positif!");
    } else {
        alert("Merci pour votre retour! Nous nous efforcerons de nous améliorer.");
    }
}