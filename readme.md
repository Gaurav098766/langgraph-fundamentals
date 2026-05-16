#### Reducers
1. Override the existing values if no custom reducers are used. Default behaviour is using reducers provided by LangGraph.
2. Do operations you need by making custom reducers. In our case we had made 2 fucntions named update_count and update_animals.
3. The custom reducers should be used in the stateSchema you make as an 2nd argument. 