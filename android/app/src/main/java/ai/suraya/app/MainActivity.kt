package ai.suraya.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

data class ChatMessage(
    val text: String,
    val fromCreator: Boolean,
)

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            MaterialTheme {
                SurayaApp()
            }
        }
    }
}

@androidx.compose.runtime.Composable
private fun SurayaApp() {
    val messages = remember {
        mutableStateListOf<ChatMessage>()
    }

    var input by remember {
        mutableStateOf("")
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text("SURAYA AI")
                },
            )
        },
    ) { padding ->

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
        ) {

            Text(
                text = "Creator Console",
                style = MaterialTheme.typography.headlineSmall,
            )

            Spacer(
                modifier = Modifier.height(12.dp),
            )

            Card(
                modifier = Modifier.fillMaxWidth(),
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                ) {
                    Text("Guardian: ACTIVE")
                    Text("Executor: READY")
                    Text("Runtime: READY")
                }
            }

            Spacer(
                modifier = Modifier.height(12.dp),
            )

            LazyColumn(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(messages) { message ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Text(
                            text = if (message.fromCreator) {
                                "Creator: ${message.text}"
                            } else {
                                "SURAYA: ${message.text}"
                            },
                            modifier = Modifier.padding(12.dp),
                        )
                    }
                }
            }

            Spacer(
                modifier = Modifier.height(8.dp),
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
            ) {
                OutlinedTextField(
                    value = input,
                    onValueChange = { input = it },
                    modifier = Modifier.weight(1f),
                    placeholder = {
                        Text("Command...")
                    },
                )

                Spacer(
                    modifier = Modifier.width(8.dp),
                )

                Button(
                    onClick = {
                        if (input.isNotBlank()) {
                            val command = input.trim()

                            messages.add(
                                ChatMessage(
                                    text = command,
                                    fromCreator = true,
                                )
                            )

                            messages.add(
                                ChatMessage(
                                    text = "Command received. Backend connection will be activated next.",
                                    fromCreator = false,
                                )
                            )

                            input = ""
                        }
                    },
                ) {
                    Text("Send")
                }
            }
        }
    }
}
