import React, {Component} from 'react';
import { ReactiveBase, DataSearch, CategorySearch, SingleRange, ResultCard, SelectedFilters, ReactiveList } from '@appbaseio/reactivesearch';

import theme from './theme';
import './App.css';
import Header from './components/Header';
import Results from './components/Results';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
        };
    }

    render() {
        return (
            <section className="container">
                <ReactiveBase
                    app="pf_idx"
                    type="courses_w_geo"
                    credentials="elastic:changeme"
                    url="http://localhost:9200"
                    theme={theme}
                >

                    <div className="flex row-reverse app-container">
                        <Header />
                        <div className="results-container">
                            <DataSearch
                                componentId="search"
                                filterLabel="Search"
                                dataField={['TITLE', 'GEOGRAPHY']}
                                queryFormat="and"
                                placeholder="Search Courses"
                                autosuggest={false}
                                iconPosition="left"
                                URLParams
                                className="data-search-container results-container"
                                innerClass={{
                                    input: 'search-input',
                                }}
                            />
                            <Results />
                        </div>
                    </div>
                </ReactiveBase>
            </section>
        );
    }
}

export default App;
