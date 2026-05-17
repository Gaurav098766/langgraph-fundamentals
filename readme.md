#### Reducers
1. It basically determine how out state variables will be updated. 
2. Override the existing values if no custom reducers are used. Default behaviour is using reducers provided by LangGraph.
3. Do operations you need by making custom reducers. In our case we had made 2 fucntions named update_count and update_animals.
4. The custom reducers should be used in the stateSchema you make as an 2nd argument. 

#### add_messages
1. add_messages is a reducer function in LangGraph that controls how the messages field in state gets updated when a node returns new messages.