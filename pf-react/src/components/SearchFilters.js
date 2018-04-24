import React from 'react';
import PropTypes from 'prop-types';
import {
	MultiDropdownList,
	MultiList,
	SingleDropdownRange,
	RangeSlider,
    DataSearch,
} from '@appbaseio/reactivesearch';


const SearchFilters = ({ visible }) => (
    <div className={`flex column filters-container ${!visible ? 'hidden' : ''}`}>
		<div className="child m10">
			<MultiList
				componentId="industry"
				dataField="TITLE.raw"
				placeholder="Enter or Select Industry"
				title="Industry"
				filterLabel="Industry"
				size={1000}
				queryFormat="or"
			/>
		</div>
		<div className="child m10">
			<MultiList
				componentId="geography"
				dataField="GEOGRAPHY.raw"
				placeholder="Enter or Select Geography"
				title="Geography"
				filterLabel="Geography"
				size={1000}
				queryFormat="or"
			/>
		</div>
    </div>
);

SearchFilters.propTypes = {
	visible: PropTypes.bool,
};

export default SearchFilters;