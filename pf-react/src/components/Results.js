import React from 'react';
import { SelectedFilters, ReactiveList } from '@appbaseio/reactivesearch';

const onData = (data) => (
    <div className="result-item" key={data.UNIQKEY}>
        <div className="flex wrap"><a className="link" href={data.LTURL} target="_blank" rel="noopener noreferrer">{data.TITLE}</a></div>
        <div className="flex wrap">{data.GEOGRAPHY}</div>
        <div className="flex wrap small">UKPRN: {data.UKPRN}</div>
        <div className="flex wrap small">KIS Course ID: {data.KISCOURSEID}</div>
        <div className="flex wrap"><a className="link small" href={data.LTURL} target="_blank" rel="noopener noreferrer">{data.LTURL}</a></div>
    </div>
);

const onResultStats = (results, time) => (
    <div className="flex justify-end">
        {results} results found in {time}ms
    </div>
);

const Results = () => (
    <div className="result-list">
        <SelectedFilters className="m1"/>
        <ReactiveList
            componentId="results"
            dataField="name"
            onData={onData}
            onResultStats={onResultStats}
            react={{
                and: ['search', 'industry', 'geography'],
            }}
            pagination
            innerClass={{
                list: 'result-list-container',
                pagination: 'result-list-pagination',
                resultsInfo: 'result-list-info',
                poweredBy: 'powered-by',
            }}
            size={6}
        />
    </div>
);

export default Results;